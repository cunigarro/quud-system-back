from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, UUID, Text, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


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

    inspections = relationship("Inspection", back_populates="project", lazy="dynamic")

    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)


class RuleType(Base):
    __tablename__ = "rule_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)


class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    rule_type_id = Column(Integer, ForeignKey("rule_types.id", ondelete="SET NULL"))
    flow_config = Column(JSON)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)

    rule_type = relationship("RuleType")


class RuleGroup(Base):
    __tablename__ = "rule_groups"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    flow_config = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)


class RuleGroupRule(Base):
    __tablename__ = "rule_group_rules"
    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("rule_groups.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())


class InspectionStatus(Base):
    __tablename__ = "inspection_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    branch = Column(String(100), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    rule_group_id = Column(Integer, ForeignKey("rule_groups.id", ondelete="SET NULL"), nullable=True)
    inspection_status_id = Column(Integer, ForeignKey("inspection_status.id", ondelete="SET NULL"), nullable=True)
    processed_at = Column(TIMESTAMP, server_default=func.now())
    result = Column(JSON, nullable=True)
    execution_info = Column(JSON, nullable=True)
    history_status = Column(JSON, default=[])

    project = relationship("Project", back_populates="inspections")
    rule_group = relationship("RuleGroup", backref="inspections", lazy="joined")
    status = relationship("InspectionStatus", backref="inspections", lazy="joined")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
