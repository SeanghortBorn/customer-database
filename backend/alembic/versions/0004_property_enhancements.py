"""add owner, website/social media, and source fields to properties

Revision ID: 0004_property_enhancements
Revises: 0003_more_features
Create Date: 2026-02-14 00:00:00.000003
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '0004_property_enhancements'
down_revision = '0003_more_features'
branch_labels = None
depends_on = None


def upgrade():
    # add owner_id foreign key to properties (references people)
    op.add_column('properties', sa.Column('owner_id', pg.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_properties_owner_id', 'properties', 'people', ['owner_id'], ['id'])
    
    # add website_social_media field
    op.add_column('properties', sa.Column('website_social_media', sa.String(), nullable=True))
    
    # add source field (where property info came from)
    op.add_column('properties', sa.Column('source', sa.String(), nullable=True))


def downgrade():
    op.drop_constraint('fk_properties_owner_id', 'properties', type_='foreignkey')
    op.drop_column('properties', 'owner_id')
    op.drop_column('properties', 'website_social_media')
    op.drop_column('properties', 'source')

