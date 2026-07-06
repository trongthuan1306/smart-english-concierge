"""
handler.py — Vocab Saver Skill Handler

This is the executable backend for the "vocab-saver" skill.
It is dynamically imported and called by the SkillRouter when the
LLM determines that the user wants to save a vocabulary word.

Convention:
    Every skill handler MUST expose a `run(**kwargs)` function.
"""

from database.database import SessionLocal
from database import crud
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def run(*, word: str = "", meaning: str = "", example: str = "", **kwargs) -> dict:
    """Save a vocabulary word to PostgreSQL database via SQLAlchemy ORM.

    Parameters
    ----------
    word : str
        The English vocabulary word to save.
    meaning : str
        The Vietnamese definition/translation.
    example : str
        An example sentence demonstrating usage.

    Returns
    -------
    dict
        A confirmation payload with the saved entry.
    """
    if not word:
        return {"status": "error", "message": "No word provided to save."}

    word = word.strip()
    meaning = meaning.strip()
    example = example.strip()

    db = SessionLocal()
    try:
        # Check for exact duplicate (case-insensitive)
        existing_vocab = crud.get_vocabulary_by_word(db, word)
        if existing_vocab:
            return {
                "status": "duplicate",
                "message": f"The word '{word}' is already in your notebook.",
            }

        # Save vocabulary
        saved_vocab = crud.save_vocabulary(db, word, meaning, example)
        
        # Build entry for response
        entry = {
            "id": saved_vocab.id,
            "word": saved_vocab.word,
            "meaning": saved_vocab.meaning,
            "example": saved_vocab.example,
            "created_at": saved_vocab.created_at.isoformat() if saved_vocab.created_at else None,
        }
        
        # Calculate total words
        total_words = len(crud.get_all_vocabulary(db))

        return {
            "status": "success",
            "message": f"✅ Saved '{word}' to your vocabulary notebook!",
            "entry": entry,
            "total_words": total_words,
        }
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Database error while saving vocabulary")
        return {"status": "error", "message": "Failed to save vocabulary due to a database error."}
    finally:
        db.close()
