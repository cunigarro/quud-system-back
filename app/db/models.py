from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, UUID, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    names = Column(String, nullable=False)
    last_names = Column(String, nullable=False)
    cellphone = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile_metadata = Column(JSONB)


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


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="SET NULL"), nullable=True)
    language_version_id = Column(Integer, ForeignKey("language_versions.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)
