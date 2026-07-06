"""
router.py — Multi-Agent Graph Router (ADK 2.0 Concept)

This module is the central orchestrator of the Smart English Concierge.
It implements three core capabilities for the Kaggle Capstone evaluation:

  1. Tool Discovery:  Automatically scans `backend/agents/skills/` at startup,
     reads every SKILL.md specification, and builds a live registry of
     available skills — no hard-coded imports required.

  2. Dynamic Routing:  Sends the user's input together with the full skill
     catalogue to the Gemini LLM (via google-genai) and lets the model
     decide which skill (if any) should handle the request.  This mirrors
     the ADK 2.0 "Graph Routing" pattern where specialised nodes are
     selected by an intelligent router node.

  3. Skill Execution:  Once a skill is chosen, the router dynamically
     imports and calls the skill's handler from its `scripts/` subdirectory,
     keeping the system fully plug-and-play.

Architecture:
  ┌────────────┐        ┌────────────┐        ┌───────────────┐
  │ User Input │──►│ SkillRouter │──►│ LLM (Gemini)  │
  └────────────┘        │  (router)  │        └──────┬────────┘
                        └─────┬──────┘               │
                              │  skill_name          │ tool_call
                              ▼                      │
                        ┌─────────────┐              │
                        │ SkillRegistry│◄─────────────┘
                        │ (discovery) │
                        └─────┬───────┘
                              │ dynamic import
                              ▼
                        ┌─────────────┐
                        │  scripts/   │
                        │  handler.py │
                        └─────────────┘

Usage:
    from agents.router import SkillRouter

    router = SkillRouter()          # scans skills/ on init
    result = await router.route("Save the word 'ephemeral'")
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


# ===========================================================================
#  Data Classes
# ===========================================================================

@dataclass
class SkillSpec:
    """Parsed representation of a single SKILL.md file."""

    name: str                     # directory name, e.g. "vocab-saver"
    description: str              # first paragraph after the heading
    full_markdown: str            # raw SKILL.md content for the LLM prompt
    directory: Path               # absolute path to the skill directory
    parameters: list[str] = field(default_factory=list)
    when_to_use: str = ""

    # ----- helpers ---------------------------------------------------------

    @property
    def function_name(self) -> str:
        """Convert the directory name into a Python-safe function name.

        Example: "vocab-saver"  →  "vocab_saver"
        """
        return self.name.replace("-", "_")

    @property
    def scripts_dir(self) -> Path:
        """Return the path to this skill's scripts/ folder."""
        return self.directory / "scripts"

    @property
    def handler_path(self) -> Path:
        """Return the expected path of the handler module."""
        return self.scripts_dir / "handler.py"

    def has_handler(self) -> bool:
        """Check whether a runnable handler.py exists."""
        return self.handler_path.is_file()


# ===========================================================================
#  SKILL.md Parser
# ===========================================================================

class SkillMarkdownParser:
    """Parses a SKILL.md file into a structured :class:`SkillSpec`.

    Supports two formats:
      • YAML-frontmatter style (``---`` delimited name/description block).
      • Simple markdown style (``# Skill: <name>`` heading).
    """

    # Patterns -----------------------------------------------------------------
    _FRONTMATTER_RE = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n",
        re.DOTALL,
    )
    _HEADING_NAME_RE = re.compile(
        r"^#\s+(?:Skill:\s*)?(.+)",
        re.MULTILINE,
    )
    _SECTION_RE = re.compile(
        r"^##\s+(.+)",
        re.MULTILINE,
    )

    # Public API ---------------------------------------------------------------

    @classmethod
    def parse(cls, skill_dir: Path) -> SkillSpec:
        """Read ``SKILL.md`` from *skill_dir* and return a :class:`SkillSpec`."""
        md_path = skill_dir / "SKILL.md"
        raw = md_path.read_text(encoding="utf-8")

        name = skill_dir.name                     # fallback: directory name
        description = ""
        when_to_use = ""
        parameters: list[str] = []

        # --- Try YAML frontmatter first ---
        fm_match = cls._FRONTMATTER_RE.match(raw)
        if fm_match:
            for line in fm_match.group(1).splitlines():
                key, _, value = line.partition(":")
                key = key.strip().lower()
                value = value.strip()
                if key == "name" and value:
                    name = value
                elif key == "description" and value:
                    description = value
        else:
            # --- Simple heading style ---
            heading = cls._HEADING_NAME_RE.search(raw)
            if heading:
                name = heading.group(1).strip()

        # --- Extract sections ---
        sections = cls._split_sections(raw)
        if "description" in sections and not description:
            description = sections["description"].strip()
        if "when to use" in sections:
            when_to_use = sections["when to use"].strip()
        if "parameters" in sections:
            parameters = cls._parse_param_list(sections["parameters"])

        return SkillSpec(
            name=skill_dir.name,          # always use dir name for routing
            description=description or name,
            full_markdown=raw,
            directory=skill_dir,
            parameters=parameters,
            when_to_use=when_to_use,
        )

    # Internals ----------------------------------------------------------------

    @classmethod
    def _split_sections(cls, text: str) -> dict[str, str]:
        """Split the markdown body into ``{heading_lower: content}`` pairs."""
        matches = list(cls._SECTION_RE.finditer(text))
        sections: dict[str, str] = {}
        for i, m in enumerate(matches):
            heading = m.group(1).strip().lower()
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections[heading] = text[start:end]
        return sections

    @classmethod
    def _parse_param_list(cls, section_text: str) -> list[str]:
        """Pull out parameter names from a markdown bullet list."""
        params: list[str] = []
        for line in section_text.splitlines():
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                # Extract the backtick-wrapped param name, e.g. `word`
                tick = re.search(r"`(\w+)`", line)
                if tick:
                    params.append(tick.group(1))
        return params


# ===========================================================================
#  Skill Registry — Auto-Discovery
# ===========================================================================

class SkillRegistry:
    """Scans the ``skills/`` directory and holds a live map of all skills.

    This class is responsible for the **Tool Discovery** requirement:
    it walks the skills directory at construction time, parses every
    SKILL.md it finds, and exposes the results as a dict keyed by
    the directory name.

    Adding a new skill is zero-code: just drop a new subdirectory with a
    SKILL.md and (optionally) a ``scripts/handler.py`` — the registry will
    pick it up automatically on the next instantiation.
    """

    def __init__(self, skills_root: Path | str) -> None:
        self._root = Path(skills_root).resolve()
        self._skills: dict[str, SkillSpec] = {}
        self._discover()

    # ----- discovery -------------------------------------------------------

    def _discover(self) -> None:
        """Walk ``skills/`` and register every valid subdirectory."""
        if not self._root.is_dir():
            logger.warning("Skills directory does not exist: %s", self._root)
            return

        for child in sorted(self._root.iterdir()):
            if not child.is_dir():
                continue
            skill_md = child / "SKILL.md"
            if not skill_md.is_file():
                logger.debug("Skipping %s — no SKILL.md found.", child.name)
                continue
            try:
                spec = SkillMarkdownParser.parse(child)
                self._skills[spec.name] = spec
                logger.info(
                    "✅ Registered skill: %-25s  (params=%s)",
                    spec.name,
                    spec.parameters or "—",
                )
            except Exception:
                logger.exception("Failed to parse SKILL.md in %s", child)

    # ----- public API -------------------------------------------------------

    @property
    def skills(self) -> dict[str, SkillSpec]:
        return dict(self._skills)

    @property
    def skill_names(self) -> list[str]:
        return list(self._skills.keys())

    def get(self, name: str) -> SkillSpec | None:
        return self._skills.get(name)

    def build_catalogue_prompt(self) -> str:
        """Render a human-readable catalogue of all skills for the LLM.

        This text is injected into the system prompt so the model understands
        which tools (skills) are available and when each one should fire.
        """
        lines: list[str] = [
            "# Available Skills (Tools)\n",
            "Below is a list of all available skills. "
            "Based on the user's message, decide which ONE skill is the best "
            "match.  If none of them is a good match, respond with the "
            '`no_matching_skill` tool call.\n',
        ]
        for spec in self._skills.values():
            lines.append(f"## {spec.name}")
            lines.append(f"**Description:** {spec.description}")
            if spec.when_to_use:
                lines.append(f"**When to use:** {spec.when_to_use}")
            if spec.parameters:
                lines.append(f"**Parameters:** {', '.join(spec.parameters)}")
            lines.append("")  # blank line separator
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._skills)

    def __repr__(self) -> str:
        return f"<SkillRegistry skills={self.skill_names}>"


# ===========================================================================
#  Dynamic Skill Executor
# ===========================================================================

class SkillExecutor:
    """Dynamically imports and runs a skill's ``scripts/handler.py``.

    Convention:
      Each handler module must expose a callable named ``run(**kwargs)``
      that accepts the parameters declared in SKILL.md and returns a result
      dict (or string).
    """

    @staticmethod
    def execute(spec: SkillSpec, params: dict[str, Any]) -> dict[str, Any]:
        """Import the skill's handler and call its ``run()`` function.

        Parameters
        ----------
        spec : SkillSpec
            The skill to execute.
        params : dict
            Keyword arguments extracted by the LLM for this skill.

        Returns
        -------
        dict
            ``{"status": "success"|"error", "skill": ..., "data": ...}``
        """
        if not spec.has_handler():
            return {
                "status": "error",
                "skill": spec.name,
                "message": (
                    f"Skill '{spec.name}' is registered but its handler "
                    f"has not been implemented yet. "
                    f"Expected file: {spec.handler_path}"
                ),
            }

        try:
            module = SkillExecutor._import_handler(spec)
            if not hasattr(module, "run"):
                return {
                    "status": "error",
                    "skill": spec.name,
                    "message": (
                        f"Handler for '{spec.name}' is missing a `run()` "
                        f"function.  Please define `def run(**kwargs)` in "
                        f"{spec.handler_path}."
                    ),
                }

            result = module.run(**params)
            return {
                "status": "success",
                "skill": spec.name,
                "data": result,
            }
        except Exception as exc:
            logger.exception("Error executing skill '%s'", spec.name)
            return {
                "status": "error",
                "skill": spec.name,
                "message": str(exc),
            }

    # ----- dynamic import ---------------------------------------------------

    @staticmethod
    def _import_handler(spec: SkillSpec):
        """Import ``scripts/handler.py`` as a module, isolated by skill name."""
        module_name = f"skill_handler_{spec.function_name}"

        # If already imported, delete it to ensure a fresh hot-reload
        if module_name in sys.modules:
            del sys.modules[module_name]

        handler_path = str(spec.handler_path)
        loader_spec = importlib.util.spec_from_file_location(
            module_name, handler_path,
        )
        module = importlib.util.module_from_spec(loader_spec)
        
        # Ensure __spec__ is set just in case
        module.__spec__ = loader_spec
        
        sys.modules[module_name] = module
        loader_spec.loader.exec_module(module)
        return module


# ===========================================================================
#  Skill Router — LLM-Powered Intent Matching
# ===========================================================================

class SkillRouter:
    """The main entry-point for the Dynamic Routing system.

    Workflow:
      1.  On instantiation, scan ``skills/`` and build a :class:`SkillRegistry`.
      2.  When :meth:`route` is called with user text:
          a. Construct a system prompt that contains the full skill catalogue.
          b. Ask the Gemini LLM to pick the best matching skill by making a
             *tool call* (function call) whose name matches a skill.
          c. If the LLM returns a tool call → execute the chosen skill.
          d. If the LLM returns plain text or ``no_matching_skill``
             → return a polite default response.

    New skills are discovered automatically — no code changes needed.
    """

    # Default path: ``backend/agents/skills/``
    _DEFAULT_SKILLS_DIR = Path(__file__).resolve().parent / "skills"

    def __init__(
        self,
        skills_dir: Path | str | None = None,
        model_name: str = "gemini-3.1-flash-lite",
    ) -> None:
        # --- Resolve skills directory ---
        self._skills_dir = Path(skills_dir) if skills_dir else self._DEFAULT_SKILLS_DIR

        # --- Build the registry (auto-discovery) ---
        self.registry = SkillRegistry(self._skills_dir)
        logger.info("Router initialised with %d skills.", len(self.registry))

        # --- Configure Google GenAI client ---
        self._model_name = model_name
        self._client = genai.Client()           # reads GEMINI_API_KEY from env

        # --- Pre-build the tool declarations for the LLM ---
        self._tools = self._build_tool_declarations()

    # -----------------------------------------------------------------------
    #  Public API
    # -----------------------------------------------------------------------

    async def route(self, user_input: str) -> dict[str, Any]:
        """Route *user_input* to the most appropriate skill.

        Returns
        -------
        dict
            A result envelope:
            ``{"status": "success"|"error"|"default", "skill": ..., "data": ...}``
        """
        if not self.registry.skills:
            logger.warning("No skills registered — returning default response.")
            return self._default_response(user_input)

        # Step 1: Ask the LLM to pick a skill via a tool/function call
        chosen_skill_name, params = await self._llm_select_skill(user_input)

        # Step 2a: No match — polite fallback
        if chosen_skill_name is None:
            return self._default_response(user_input)

        # Step 2b: Skill matched — look it up in the registry
        # NOTE: LLM returns underscored names (e.g. "vocab_saver") because
        # FunctionDeclaration names must be valid identifiers, but the registry
        # keys use the original hyphenated directory name (e.g. "vocab-saver").
        # We try both forms to ensure a match.
        spec = self.registry.get(chosen_skill_name)
        if spec is None:
            hyphenated = chosen_skill_name.replace("_", "-")
            spec = self.registry.get(hyphenated)
        if spec is None:
            logger.warning(
                "LLM chose skill '%s' which is not in the registry.",
                chosen_skill_name,
            )
            return self._default_response(user_input)

        # Step 3: Execute the skill handler
        logger.info(
            "🎯 Routing to skill '%s' with params: %s",
            spec.name, params,
        )
        result = SkillExecutor.execute(spec, params)
        return result

    def list_skills(self) -> list[dict[str, str]]:
        """Return a JSON-friendly list of all registered skills."""
        return [
            {
                "name": s.name,
                "description": s.description,
                "has_handler": s.has_handler(),
                "parameters": s.parameters,
            }
            for s in self.registry.skills.values()
        ]

    # -----------------------------------------------------------------------
    #  LLM Interaction
    # -----------------------------------------------------------------------

    async def _llm_select_skill(
        self,
        user_input: str,
    ) -> tuple[str | None, dict[str, Any]]:
        """Send the user input + skill catalogue to Gemini and return the
        chosen skill name and extracted parameters.

        The model is instructed to respond exclusively via a tool call
        (function call) whose name corresponds to one of the registered
        skills.  If nothing matches, it should call ``no_matching_skill``.
        """
        system_prompt = self._build_system_prompt()

        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=self._tools,
                    temperature=0.1,          # low temperature → deterministic routing
                ),
            )
        except Exception:
            logger.exception("LLM call failed during skill selection.")
            return None, {}

        # --- Parse the response for a function call ---
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    fn = part.function_call
                    skill_name = fn.name
                    params = dict(fn.args) if fn.args else {}

                    # "no_matching_skill" is our sentinel tool
                    if skill_name == "no_matching_skill":
                        logger.info("LLM decided: no matching skill.")
                        return None, {}

                    return skill_name, params

        # If the model returned plain text instead of a tool call
        logger.info("LLM returned text (no tool call) — treating as no match.")
        return None, {}

    # -----------------------------------------------------------------------
    #  Prompt & Tool Declaration Builders
    # -----------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        """Compose the system instruction sent to the LLM."""
        catalogue = self.registry.build_catalogue_prompt()
        logger.info("=== CATALOGUE SENT TO LLM ===\n%s", catalogue)   # thêm dòng này

        return (
            "You are a precise intent-routing engine inside the "
            "Smart English Concierge system.\n\n"
            "Your ONLY job is to analyze the user's message and decide "
            "which skill (tool) should handle it.  You MUST reply "
            "exclusively with a single tool/function call — never with "
            "plain text.\n\n"
            "Rules:\n"
            "1. Pick the ONE skill whose 'When to use' clause best matches "
            "   the user's intent.\n"
            "2. Extract the required parameters from the user's message and "
            "   pass them as arguments in the tool call.\n"
            "3. If the user's message does not clearly match ANY skill, "
            "   call the `no_matching_skill` tool.\n"
            "4. Never invent skills that are not listed below.\n\n"
            f"{catalogue}"
        )

    def _build_tool_declarations(self) -> list[types.Tool]:
        """Convert every registered skill into a Gemini Tool declaration.

        Each skill becomes a function the LLM can "call".  We also add
        a ``no_matching_skill`` sentinel function for the fallback case.
        """
        function_declarations: list[types.FunctionDeclaration] = []

        for spec in self.registry.skills.values():
            # Build a properties dict from the skill's parameter list
            properties: dict[str, Any] = {}
            for param in spec.parameters:
                properties[param] = types.Schema(
                    type=types.Type.STRING,
                    description=f"The '{param}' parameter for the {spec.name} skill.",
                )

            # If the skill had no explicit params, accept free-form 'input'
            if not properties:
                properties["input"] = types.Schema(
                    type=types.Type.STRING,
                    description="The user's input text to be processed by this skill.",
                )

            func_decl = types.FunctionDeclaration(
                name=spec.name.replace("-", "_"),
                description=spec.description,
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties=properties,
                ),
            )
            function_declarations.append(func_decl)

        # --- Sentinel: no_matching_skill ---
        function_declarations.append(
            types.FunctionDeclaration(
                name="no_matching_skill",
                description=(
                    "Call this when the user's message does not match any "
                    "of the available skills."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "reason": types.Schema(
                            type=types.Type.STRING,
                            description="Brief explanation of why no skill matched.",
                        ),
                    },
                ),
            )
        )

        return [types.Tool(function_declarations=function_declarations)]

    # -----------------------------------------------------------------------
    #  Default / Fallback Response
    # -----------------------------------------------------------------------

    @staticmethod
    def _default_response(user_input: str) -> dict[str, Any]:
        """Return a friendly message when no skill matches the user's intent."""
        return {
            "status": "default",
            "skill": None,
            "message": (
                "I'm not quite sure how to help with that specific request. "
                "Here are some things I can do:\n"
                "  • 📖 Check your English grammar\n"
                "  • 📝 Save new vocabulary words\n"
                "  • 🔊 Pronounce words for you\n"
                "  • 🛡️ Redact personal information\n\n"
                "Feel free to try rephrasing your question!"
            ),
            "original_input": user_input,
        }


# ===========================================================================
#  Module-Level Convenience
# ===========================================================================

# Pre-instantiate a router for simple imports:
#     from agents.router import router
#     result = await router.route("...")
#
# This only runs when the module is imported while GEMINI_API_KEY is set.
# If the key is missing the import still succeeds; create the router manually
# after configuring the environment.

router: SkillRouter | None = None

def get_router(skills_dir: Path | str | None = None) -> SkillRouter:
    """Lazy-singleton accessor for the global :class:`SkillRouter` instance."""
    global router
    if router is None:
        router = SkillRouter(skills_dir=skills_dir)
    return router
