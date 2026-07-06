# Skill: vocab-saver

## Description
This tool is used to extract new vocabulary words from the user's conversation and save them into the local vocabulary database (`saved_vocabulary.json`).

## Parameters
- `word` (string): The English vocabulary word to be saved.
- `meaning` (string): The definition or translation of the word in Vietnamese.
- `example` (string): An example sentence illustrating the usage of the word in English.

## When to use
- Use this tool when the user explicitly asks to "save this word," asks for the definition of a word, or when the Agent identifies a new vocabulary item that would be beneficial for the user to store in their notebook.

## Example Usage
- **Input:** `save_vocabulary(word="Serendipity", meaning="Sự tình cờ may mắn", example="Our meeting was pure serendipity.")`
- **Expected Output:** A success confirmation message, and the word is appended to the JSON database with an automatic update to the analytics counters.