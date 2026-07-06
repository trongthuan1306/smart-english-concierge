# Skill: voice-synthesis-trigger

## Description
This tool triggers the Text-to-Speech (TTS) engine to synthesize natural-sounding audio for specific English words or sentences.

## Parameters
- `text` (string): The text to be converted into audio.
- `voice_type` (string): Optional parameter to specify accent (e.g., "en-US", "en-GB").

## When to use
- Use this when the user clicks the "Speak" button in the interface or requests to hear the pronunciation of a specific vocabulary word.

## Example Usage
- **Input:** `synthesize_voice(text="Serendipity", voice_type="en-US")`
- **Expected Output:** A link or stream to the generated audio file for the user to playback.