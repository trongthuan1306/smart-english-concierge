"""
test_router_simulation.py — Giả lập 3 test cases cho SkillRouter

Test này KHÔNG cần API key thật. Nó mock (giả lập) phản hồi của LLM
để kiểm tra 3 luồng xử lý chính:

  Case 1: LLM trả về tool call "vocab_saver"  → Lưu từ vựng
  Case 2: LLM trả về tool call "grammar_checker" → Sửa ngữ pháp
  Case 3: LLM trả về tool call "no_matching_skill" → Không khớp skill nào

Chạy:
  cd backend
  python -m pytest tests/test_router_simulation.py -v
  
  hoặc chạy trực tiếp:
  python tests/test_router_simulation.py
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# ---------------------------------------------------------------------------
# Ensure the backend package is importable
# ---------------------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from agents.router import SkillRegistry, SkillExecutor, SkillRouter, SkillSpec

# ---------------------------------------------------------------------------
#  Helper: Build a fake Gemini response containing a function_call
# ---------------------------------------------------------------------------

def _make_fake_response(function_name: str, args: dict | None = None):
    """Create a mock object that mimics the Gemini GenerateContentResponse
    with a single function_call part.

    This mirrors the structure:
        response.candidates[0].content.parts[0].function_call.name
        response.candidates[0].content.parts[0].function_call.args
    """
    fn_call = MagicMock()
    fn_call.name = function_name
    fn_call.args = args or {}

    part = MagicMock()
    part.function_call = fn_call

    candidate = MagicMock()
    candidate.content.parts = [part]

    response = MagicMock()
    response.candidates = [candidate]
    return response


# ===========================================================================
#  CASE 1: LLM gọi tool "vocab_saver" → lưu từ vựng
# ===========================================================================

async def test_case_1_vocab_saver():
    """
    Giả lập: User nói "Save the word 'Serendipity'"
    Kỳ vọng: Router nhận tool call "vocab_saver", tìm thấy skill "vocab-saver",
             và gọi handler (hoặc báo handler chưa implement nếu chưa có scripts/).
    """
    print("\n" + "=" * 70)
    print("🧪 CASE 1: Gọi tool lưu từ vựng (vocab_saver)")
    print("=" * 70)

    user_input = "Save the word 'Serendipity', it means 'sự tình cờ may mắn'"

    # Giả lập LLM trả về function_call: vocab_saver(word=..., meaning=..., example=...)
    fake_response = _make_fake_response(
        function_name="vocab_saver",
        args={
            "word": "Serendipity",
            "meaning": "Sự tình cờ may mắn",
            "example": "Our meeting was pure serendipity.",
        },
    )

    # Patch genai.Client để không gọi API thật
    with patch("agents.router.genai.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.models.generate_content.return_value = fake_response

        router = SkillRouter()
        result = await router.route(user_input)

    print(f"  📥 Input:  \"{user_input}\"")
    print(f"  🏷️  Skill:  {result.get('skill')}")
    print(f"  📊 Status: {result.get('status')}")

    if result["status"] == "success":
        print(f"  ✅ Data:   {result.get('data')}")
    elif result["status"] == "error":
        print(f"  ⚠️  Msg:    {result.get('message')}")

    # Assertions
    assert result["skill"] == "vocab-saver", f"Expected 'vocab-saver', got '{result.get('skill')}'"
    assert result["status"] in ("success", "error"), f"Unexpected status: {result['status']}"
    print("  ✅ PASSED — Router correctly routed to vocab-saver skill!")
    return result


# ===========================================================================
#  CASE 2: LLM gọi tool "grammar_checker" → sửa ngữ pháp
# ===========================================================================

async def test_case_2_grammar_checker():
    """
    Giả lập: User nói "Check my grammar: I has a apple"
    Kỳ vọng: Router nhận tool call "grammar_checker", tìm skill "grammar-checker".
    """
    print("\n" + "=" * 70)
    print("🧪 CASE 2: Gọi tool sửa ngữ pháp (grammar_checker)")
    print("=" * 70)

    user_input = "Check my grammar: I has a apple yesterday."

    # Giả lập LLM trả về function_call: grammar_checker(input_text=...)
    fake_response = _make_fake_response(
        function_name="grammar_checker",
        args={
            "input_text": "I has a apple yesterday.",
        },
    )

    with patch("agents.router.genai.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.models.generate_content.return_value = fake_response

        router = SkillRouter()
        result = await router.route(user_input)

    print(f"  📥 Input:  \"{user_input}\"")
    print(f"  🏷️  Skill:  {result.get('skill')}")
    print(f"  📊 Status: {result.get('status')}")

    if result["status"] == "error":
        print(f"  ⚠️  Msg:    {result.get('message')}")

    # Assertions
    assert result["skill"] == "grammar-checker", f"Expected 'grammar-checker', got '{result.get('skill')}'"
    assert result["status"] in ("success", "error"), f"Unexpected status: {result['status']}"
    print("  ✅ PASSED — Router correctly routed to grammar-checker skill!")
    return result


# ===========================================================================
#  CASE 3: LLM gọi "no_matching_skill" → không khớp skill nào
# ===========================================================================

async def test_case_3_no_match():
    """
    Giả lập: User nói "What's the weather today?"
    Kỳ vọng: Router nhận tool call "no_matching_skill" và trả về default response.
    """
    print("\n" + "=" * 70)
    print("🧪 CASE 3: Không khớp skill nào (no_matching_skill)")
    print("=" * 70)

    user_input = "What's the weather like today in Ho Chi Minh City?"

    # Giả lập LLM trả về function_call: no_matching_skill(reason=...)
    fake_response = _make_fake_response(
        function_name="no_matching_skill",
        args={
            "reason": "The user is asking about weather, which is not related to any English learning skill.",
        },
    )

    with patch("agents.router.genai.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.models.generate_content.return_value = fake_response

        router = SkillRouter()
        result = await router.route(user_input)

    print(f"  📥 Input:  \"{user_input}\"")
    print(f"  🏷️  Skill:  {result.get('skill')}")
    print(f"  📊 Status: {result.get('status')}")
    print(f"  💬 Msg:    {result.get('message', '')[:100]}...")

    # Assertions
    assert result["status"] == "default", f"Expected 'default', got '{result['status']}'"
    assert result["skill"] is None, f"Expected None, got '{result.get('skill')}'"
    print("  ✅ PASSED — Router correctly returned default response!")
    return result


# ===========================================================================
#  Bonus: Test SkillRegistry discovery (không cần LLM)
# ===========================================================================

def test_bonus_registry_discovery():
    """Kiểm tra rằng SkillRegistry đã scan đúng tất cả skill directories."""
    print("\n" + "=" * 70)
    print("🧪 BONUS: Kiểm tra SkillRegistry auto-discovery")
    print("=" * 70)

    skills_dir = Path(__file__).resolve().parents[1] / "agents" / "skills"
    registry = SkillRegistry(skills_dir)

    print(f"  📂 Skills dir: {skills_dir}")
    print(f"  📦 Registered:  {len(registry)} skills")
    print(f"  📋 Skill list:")
    for name, spec in registry.skills.items():
        has_handler = "✅" if spec.has_handler() else "❌"
        params = ", ".join(spec.parameters) if spec.parameters else "—"
        print(f"       {has_handler} {name:<30} params=[{params}]")

    assert len(registry) > 0, "No skills were discovered!"
    assert registry.get("vocab-saver") is not None, "vocab-saver not found!"
    assert registry.get("grammar-checker") is not None, "grammar-checker not found!"
    print(f"\n  ✅ PASSED — {len(registry)} skills auto-discovered successfully!")


# ===========================================================================
#  Runner
# ===========================================================================

async def main():
    """Chạy tất cả test cases."""
    print("🚀 Smart English Concierge — Router Simulation Test")
    print("   Tất cả test đều MOCK (giả lập) LLM, không cần API key.\n")

    # Bonus: Test discovery trước (không cần async)
    test_bonus_registry_discovery()

    # 3 test cases chính
    await test_case_1_vocab_saver()
    await test_case_2_grammar_checker()
    await test_case_3_no_match()

    print("\n" + "=" * 70)
    print("🎉 TẤT CẢ 4 TEST CASES ĐỀU PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
