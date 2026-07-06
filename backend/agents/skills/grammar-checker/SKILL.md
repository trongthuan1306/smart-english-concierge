# Skill: grammar-checker

## Description
This tool analyzes the user's English input for grammatical, syntactical, and punctuation errors. It provides corrected versions along with brief explanations of the mistakes.

## Parameters
- `input_text` (string): The user's English sentence that needs to be checked.

## When to use
- Call this whenever the user asks for feedback on their writing, or when the Agent detects potential grammatical issues in a long-form response during an English practice session.

## Example Usage
- **Input:** `check_grammar(input_text="I has a apple yesterday.")`
- **Expected Output:** `{"corrected_text": "I had an apple yesterday.", "explanation": "Changed 'has' to 'had' for past tense and 'a' to 'an' before a vowel sound."}`