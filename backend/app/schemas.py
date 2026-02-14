from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class UserBase(BaseModel):
    id: Optional[UUID]
    email: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True


class PersonCreate(BaseModel):
    first_name: str
    last_name: Optional[str]
    phone: Optional[str]
    telegram: Optional[str]
    email: Optional[str]
    title: Optional[str]
    notes: Optional[str]
    custom: Optional[Dict[str, Any]] = Field(default_factory=dict)


class PersonOut(PersonCreate):
    id: UUID
    org_id: UUID
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class UnitCreate(BaseModel):
    unit_no: str
    size: Optional[int]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    monthly_rent: Optional[float]
    status: Optional[str] = "available"


class UnitOut(UnitCreate):
    id: UUID
    property_id: UUID
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class PropertyCreate(BaseModel):
    name: str
    type: Optional[str]
    address: Optional[str]
    google_maps_url: Optional[str]
    reference_link: Optional[str]
    notes: Optional[str]
    currency: Optional[str] = "USD"
    services_included: Optional[Dict[str, bool]] = Field(default_factory=dict)
    amenity_tags: Optional[List[str]] = Field(default_factory=list)


class PropertyOut(PropertyCreate):
    id: UUID
    org_id: UUID
    unit_count: int = 0
    created_at: Optional[datetime]
    units: Optional[List[UnitOut]] = []

    class Config:
        orm_mode = True


# --- Authentication / user schemas ---
class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str]


class UserOut(BaseModel):
    id: Optional[UUID]
    email: Optional[str]
    name: Optional[str]
    role: Optional[str]
    org_id: Optional[UUID]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str]
    exp: Optional[int]


class ShareCreate(BaseModel):
    resource_type: str
    resource_id: UUID
    grantee_email: str
    role: Optional[str] = 'viewer'
