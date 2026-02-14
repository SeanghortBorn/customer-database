import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    JSON,
    Numeric,
    CHAR,
)
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship

from app.db.base import Base


# Cross-dialect GUID type: uses Postgres UUID where available, otherwise CHAR(36)
class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID as PG_UUID
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == 'postgresql':
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    name = Column(String, nullable=True)
    role = Column(String, default="editor")
    created_at = Column(DateTime, default=datetime.utcnow)

    org = relationship("Organization")


class Person(Base):
    __tablename__ = "people"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    telegram = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    title = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    custom = Column(JSON, nullable=True, default={})
    created_by = Column(GUID(), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    org = relationship("Organization")


class Property(Base):
    __tablename__ = "properties"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)  # apartment, rental_room, house, etc.
    address = Column(String, nullable=True)
    google_maps_url = Column(String, nullable=True)
    reference_link = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    unit_count = Column(Integer, default=0)
    amenity_tags = Column(JSON, nullable=True, default=list)
    services_included = Column(JSON, nullable=True, default=dict)  # structured booleans
    currency = Column(String, nullable=False, default="USD")

    # optional geolocation for map view
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    created_by = Column(GUID(), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    org = relationship("Organization")
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")


class Unit(Base):
    __tablename__ = "units"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    property_id = Column(GUID(), ForeignKey("properties.id"), nullable=False, index=True)
    unit_no = Column(String, nullable=False)
    size = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    monthly_rent = Column(Numeric(12, 2), nullable=True)
    status = Column(String, default="available")  # available | occupied | maintenance
    created_at = Column(DateTime, default=datetime.utcnow)

    property = relationship("Property", back_populates="units")




class Comment(Base):
    __tablename__ = "comments"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    resource_type = Column(String, nullable=False)
    resource_id = Column(GUID(), nullable=False)
    author_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    actor_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=True)
    resource_id = Column(GUID(), nullable=True)
    diff = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Teams & invitations (basic)
class Team(Base):
    __tablename__ = "teams"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    team_id = Column(GUID(), ForeignKey("teams.id"), nullable=False)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")
    created_at = Column(DateTime, default=datetime.utcnow)


class Invite(Base):
    __tablename__ = "invites"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False, default="editor")
    token = Column(String, nullable=False, unique=True)
    accepted_by = Column(GUID(), ForeignKey("users.id"), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Extend ResourceShare with optional link token for share-by-link
class ResourceShare(Base):
    __tablename__ = "resource_shares"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    resource_type = Column(String, nullable=False)  # 'person' | 'property'
    resource_id = Column(GUID(), nullable=False)
    grantee_type = Column(String, default="user")  # user | team | link
    grantee_id = Column(GUID(), nullable=True)
    role = Column(String, nullable=False)  # viewer | commenter | editor
    link_token = Column(String, nullable=True, unique=True)
    view_count = Column(Integer, default=0)
    max_views = Column(Integer, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Unit price / rent history
class UnitPriceHistory(Base):
    __tablename__ = "unit_price_history"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    unit_id = Column(GUID(), ForeignKey("units.id"), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String, nullable=False)
    effective_date = Column(DateTime, nullable=True)
    created_by = Column(GUID(), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Saved views for lists/filters
class SavedView(Base):
    __tablename__ = "saved_views"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    org_id = Column(GUID(), ForeignKey("organizations.id"), nullable=False)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)  # people | properties
    filters = Column(JSON, nullable=True)
    columns = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
