"""
handler.py — Grammar Checker Skill Handler

This is the executable backend for the "grammar-checker" skill.
It uses the Gemini LLM to analyze the user's input for grammatical, 
syntactical, and punctuation errors, returning a corrected version 
and an explanation.

Convention:
    Every skill handler MUST expose a `run(**kwargs)` function.
"""

import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

def run(*, input_text: str = "", **kwargs) -> dict:
    """Analyze and correct English grammar using the Gemini API.

    Parameters
    ----------
    input_text : str
        The English sentence/text to be checked.

    Returns
    -------
    dict
        A dictionary containing 'corrected_text' and 'explanation',
        or an error status if the API call fails.
    """
    if not input_text:
        return {"status": "error", "message": "No input_text provided to check."}

    try:
        # Initialize the official Gemini SDK client (reads GEMINI_API_KEY from env)
        client = genai.Client()
        
        system_instruction = (
            "You are an expert English grammar checker. "
            "Analyze the user's English input for grammatical, syntactical, "
            "and punctuation errors. "
            "Provide the corrected version and a brief explanation of the mistakes."
        )
        
        # We enforce a strict JSON schema for the response
        response_schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "corrected_text": types.Schema(
                    type=types.Type.STRING,
                    description="The grammatically corrected text."
                ),
                "explanation": types.Schema(
                    type=types.Type.STRING,
                    description="A brief explanation of what was changed and why."
                )
            },
            required=["corrected_text", "explanation"]
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=input_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=response_schema,
            )
        )
        
        result_text = response.text.strip()
        
        # Parse the JSON response
        try:
            parsed_result = json.loads(result_text)
            return {
                "corrected_text": parsed_result.get("corrected_text", input_text),
                "explanation": parsed_result.get("explanation", "No changes needed.")
            }
        except json.JSONDecodeError as exc:
            logger.error(f"Failed to parse LLM response as JSON: {result_text}")
            return {
                "status": "error", 
                "message": f"Invalid JSON format returned from LLM: {str(exc)}"
            }

    except Exception as exc:
        logger.exception("Error calling Gemini API in grammar-checker")
        return {
            "status": "error",
            "message": str(exc)
        }
