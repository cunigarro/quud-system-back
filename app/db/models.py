from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    UUID,
    Text,
    JSON,
    Enum as PgEnum,
    func,
    Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.db.database import Base
from app.db.enums import RuleDimensionEnum


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

    inspections = relationship("Inspection", back_populates="owner", lazy="dynamic")


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    uuid = Column(UUID, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP)

    projects = relationship("Project", back_populates="language")
    versions = relationship("LanguageVersion", back_populates="language")


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
    projects = relationship("Project", back_populates="language_version")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="SET NULL"), nullable=True)
    language_version_id = Column(Integer, ForeignKey("language_versions.id", ondelete="SET NULL"), nullable=True)

    inspections = relationship("Inspection", back_populates="project", lazy="dynamic")
    language = relationship("Language", back_populates="projects")
    language_version = relationship("LanguageVersion", back_populates="projects")

    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)


class RuleType(Base):
    __tablename__ = "rule_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    dimension = Column(PgEnum(RuleDimensionEnum, name="rule_dimension", create_type=False))
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
    group_rules = relationship("RuleGroupRule", back_populates="rule")
    inspection_rules = relationship("InspectionRule", back_populates="rule")


class RuleGroup(Base):
    __tablename__ = "rule_groups"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    flow_config = Column(JSON, nullable=True)
    attributes_weights = Column(JSON, nullable=True)
    paradigm_weights = Column(JSON, nullable=True)
    alfa = Column(Float)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(TIMESTAMP, nullable=True)

    group_rules = relationship("RuleGroupRule", back_populates="group")


class RuleGroupRule(Base):
    __tablename__ = "rule_group_rules"
    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("rule_groups.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

    group = relationship("RuleGroup", back_populates="group_rules")
    rule = relationship("Rule", back_populates="group_rules")


class InspectionStatus(Base):
    __tablename__ = "inspection_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    branch = Column(String(100), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    rule_group_id = Column(Integer, ForeignKey("rule_groups.id", ondelete="SET NULL"), nullable=True)
    inspection_status_id = Column(Integer, ForeignKey("inspection_status.id", ondelete="SET NULL"), nullable=True)
    processed_at = Column(TIMESTAMP, server_default=func.now())
    error = Column(Text, nullable=True)
    execution_info = Column(JSON, nullable=True)
    history_status = Column(JSON, default=[])
    validations = Column(JSON, default=[])
    notification_info = Column(JSON, default={})

    total_score = Column(Float, default=0)
    total_paradigm = Column(Float, default=0)
    total_attributes = Column(Float, default=0)

    project = relationship("Project", back_populates="inspections")
    owner = relationship("User", back_populates="inspections")
    rule_group = relationship("RuleGroup", backref="inspections", lazy="joined")
    status = relationship("InspectionStatus", backref="inspections", lazy="joined")
    inspection_rules = relationship("InspectionRule", back_populates="inspection", cascade="all, delete-orphan")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)


class InspectionRule(Base):
    __tablename__ = "inspection_rule"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="SET NULL"), nullable=True)
    calification = Column(Float)
    comments = Column(JSON, default=[])
    message = Column(Text, nullable=True)
    details = Column(JSON, nullable={})

    inspection = relationship("Inspection", back_populates="inspection_rules")
    rule = relationship("Rule", back_populates="inspection_rules")
