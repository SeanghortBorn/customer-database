from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, Dict, List
from datetime import datetime
from uuid import UUID

# Workspace Schemas
class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = {}

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_by: Optional[UUID]
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Workspace Membership Schemas
class InviteCreate(BaseModel):
    email: EmailStr
    role: str = Field(default='member', pattern='^(owner|admin|editor|member)$')

class MembershipResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    user_id: Optional[UUID]
    role: str
    status: str
    invite_email: Optional[str]
    invited_at: Optional[datetime]
    accepted_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    role: str = Field(pattern='^(owner|admin|editor|member)$')

# List Schemas
class ListCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None

class ListResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    description: Optional[str]
    position: Optional[int]
    created_by: Optional[UUID]
    archived_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Column Schemas
class ColumnCreate(BaseModel):
    key: str
    name: str
    type: str
    position: Optional[int] = None
    is_required: bool = False
    is_unique: bool = False
    config: Optional[Dict[str, Any]] = {}

class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    position: Optional[int] = None
    is_required: Optional[bool] = None
    is_unique: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class ColumnResponse(BaseModel):
    id: UUID
    list_id: UUID
    key: str
    name: str
    type: str
    position: Optional[int]
    is_required: bool
    is_unique: bool
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Item Schemas
class ItemCreate(BaseModel):
    title: Optional[str] = None
    values: Optional[Dict[str, Any]] = {}

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    values: Optional[Dict[str, Any]] = None
    position: Optional[int] = None

class ItemResponse(BaseModel):
    id: UUID
    list_id: UUID
    title: Optional[str]
    values: Dict[str, Any]
    position: Optional[int]
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Relationship Schemas
class RelationshipCreate(BaseModel):
    name: str
    target_list_id: UUID
    relationship_type: str = Field(pattern='^(one_to_many|many_to_many)$')

class RelationshipResponse(BaseModel):
    id: UUID
    list_id: UUID
    name: str
    target_list_id: UUID
    relationship_type: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RelationshipLinkCreate(BaseModel):
    source_item_id: UUID
    target_item_id: UUID

class RelationshipLinkResponse(BaseModel):
    id: UUID
    relationship_id: UUID
    source_item_id: UUID
    target_item_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Comment Schemas
class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: UUID
    item_id: UUID
    user_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    user_id: Optional[UUID]
    action: str
    entity_type: Optional[str]
    entity_id: Optional[UUID]
    metadata: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
