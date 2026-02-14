"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-14 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'organizations',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'people',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('telegram', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('custom', sa.JSON(), nullable=True),
        sa.Column('created_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'properties',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('google_maps_url', sa.String(), nullable=True),
        sa.Column('reference_link', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('unit_count', sa.Integer(), nullable=True),
        sa.Column('amenity_tags', sa.JSON(), nullable=True),
        sa.Column('services_included', sa.JSON(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('created_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'units',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('property_id', pg.UUID(as_uuid=True), sa.ForeignKey('properties.id'), nullable=False),
        sa.Column('unit_no', sa.String(), nullable=False),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('monthly_rent', sa.Numeric(12,2), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'resource_shares',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('resource_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('grantee_type', sa.String(), nullable=True),
        sa.Column('grantee_id', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'comments',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('resource_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('author_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'activity_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('actor_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=True),
        sa.Column('resource_id', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('diff', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('activity_logs')
    op.drop_table('comments')
    op.drop_table('resource_shares')
    op.drop_table('units')
    op.drop_table('properties')
    op.drop_table('people')
    op.drop_table('users')
    op.drop_table('organizations')
