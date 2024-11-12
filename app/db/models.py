from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, UUID, Text
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uuid = Column(UUID, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    versions = relationship('LanguageVersion', back_populates='language')


class LanguageVersion(Base):
    __tablename__ = 'language_versions'

    id = Column(Integer, primary_key=True)
    language_id = Column(
        Integer, ForeignKey('languages.id', ondelete='CASCADE')
    )
    version = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    language = relationship('Language', back_populates='versions')
