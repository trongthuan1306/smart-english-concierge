from sqlalchemy.orm import Session
from . import models

def get_all_vocabulary(db: Session):
    return db.query(models.Vocabulary).order_by(models.Vocabulary.created_at.desc()).all()

def get_vocabulary_by_word(db: Session, word: str):
    return db.query(models.Vocabulary).filter(models.Vocabulary.word.ilike(word)).first()

def save_vocabulary(db: Session, word: str, meaning: str, example: str = None):
    db_vocab = models.Vocabulary(word=word, meaning=meaning, example=example)
    db.add(db_vocab)
    db.commit()
    db.refresh(db_vocab)
    return db_vocab

def search_vocabulary(db: Session, search_term: str):
    return db.query(models.Vocabulary).filter(models.Vocabulary.word.ilike(f"%{search_term}%")).all()
