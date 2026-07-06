# Skill: pii-redactor

## Description
This tool detects and masks sensitive personal information (PII) such as phone numbers, email addresses, and home addresses in a piece of text provided by the user, upon request.

## Parameters
- `text` (string): The text containing potential sensitive information that the user wants redacted.

## When to use
- Call this only when the user explicitly asks to redact, hide, mask, or remove sensitive personal information (phone numbers, emails, addresses) from a piece of text they provide.
- Do NOT call this for general grammar checks, vocabulary requests, or other unrelated tasks — only when PII redaction is the clear intent.

## Example Usage
- **Input:** `pii_redactor(text="My phone number is 0901234567 and email is abc@gmail.com")`
- **Expected Output:** `{"redacted_text": "My phone number is [REDACTED_PHONE] and email is [REDACTED_EMAIL]"}`