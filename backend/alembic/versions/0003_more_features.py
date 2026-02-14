"""add saved_views, share counters, property geolocation

Revision ID: 0003_more_features
Revises: 0002_features_and_rls
Create Date: 2026-02-14 00:00:00.000002
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '0003_more_features'
down_revision = '0002_features_and_rls'
branch_labels = None
depends_on = None


def upgrade():
    # add view_count and max_views to resource_shares
    op.add_column('resource_shares', sa.Column('view_count', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('resource_shares', sa.Column('max_views', sa.Integer(), nullable=True))

    # add lat/lng to properties
    op.add_column('properties', sa.Column('latitude', sa.Numeric(9,6), nullable=True))
    op.add_column('properties', sa.Column('longitude', sa.Numeric(9,6), nullable=True))

    # saved_views table
    op.create_table(
        'saved_views',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('filters', sa.JSON(), nullable=True),
        sa.Column('columns', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('saved_views')
    op.drop_column('properties', 'longitude')
    op.drop_column('properties', 'latitude')
    op.drop_column('resource_shares', 'max_views')
    op.drop_column('resource_shares', 'view_count')
