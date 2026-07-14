import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./ai_translator.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)  # MD5 hash of file content
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to notes
    notes = relationship("AINote", back_populates="document", cascade="all, delete-orphan")

class AINote(Base):
    __tablename__ = "ai_notes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    selection_text = Column(Text, nullable=False)
    position_metadata = Column(Text, nullable=False)  # JSON string: {"page": 1, "rect": [...]}
    chat_history = Column(Text, nullable=False)        # JSON string of messages list
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship to document
    document = relationship("Document", back_populates="notes")

def init_db():
    print("Initializing SQLite Database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
