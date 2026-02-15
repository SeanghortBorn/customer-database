from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..database import Base

class Workspace(Base):
    __tablename__ = 'workspaces'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_by = Column(UUID(as_uuid=True))
    settings = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class WorkspaceMembership(Base):
    __tablename__ = 'workspace_memberships'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True))
    role = Column(Enum('owner', 'admin', 'editor', 'member', name='workspace_role'), nullable=False, default='member')
    status = Column(Enum('invited', 'accepted', 'revoked', name='invite_status'), nullable=False, default='invited')
    invite_token = Column(String)
    invite_email = Column(String)
    invited_by = Column(UUID(as_uuid=True))
    invited_at = Column(DateTime(timezone=True))
    accepted_at = Column(DateTime(timezone=True))
    revoked_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class List(Base):
    __tablename__ = 'lists'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    position = Column(Integer)
    created_by = Column(UUID(as_uuid=True))
    archived_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Column_(Base):
    __tablename__ = 'columns'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    list_id = Column(UUID(as_uuid=True), ForeignKey('lists.id', ondelete='CASCADE'), nullable=False)
    key = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    position = Column(Integer)
    is_required = Column(Boolean, nullable=False, default=False)
    is_unique = Column(Boolean, nullable=False, default=False)
    config = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    list_id = Column(UUID(as_uuid=True), ForeignKey('lists.id', ondelete='CASCADE'), nullable=False)
    title = Column(Text)
    values = Column(JSONB, default={})
    position = Column(Integer)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    archived_at = Column(DateTime(timezone=True))

class Relationship(Base):
    __tablename__ = 'relationships'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    list_id = Column(UUID(as_uuid=True), ForeignKey('lists.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    target_list_id = Column(UUID(as_uuid=True), ForeignKey('lists.id', ondelete='CASCADE'), nullable=False)
    relationship_type = Column(Enum('one_to_many', 'many_to_many', name='relationship_type'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RelationshipLink(Base):
    __tablename__ = 'relationship_links'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_id = Column(UUID(as_uuid=True), ForeignKey('relationships.id', ondelete='CASCADE'), nullable=False)
    source_item_id = Column(UUID(as_uuid=True), ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    target_item_id = Column(UUID(as_uuid=True), ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True))
    action = Column(Text, nullable=False)
    entity_type = Column(Text)
    entity_id = Column(UUID(as_uuid=True))
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())