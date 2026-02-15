"""Add lists columns and items

Revision ID: 2a3b4c5d6e7f
Revises: 9071965ca8fd
Create Date: 2026-02-15 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2a3b4c5d6e7f'
down_revision: Union[str, None] = '9071965ca8fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create lists table
    op.create_table('lists',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('workspace_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=True),
        sa.Column('archived_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_lists_workspace', 'lists', ['workspace_id'])
    op.create_index('idx_lists_workspace_archived', 'lists', ['workspace_id', 'archived_at'])

    # Create columns table
    op.create_table('columns',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('list_id', sa.UUID(), nullable=False),
        sa.Column('key', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('is_required', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_unique', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('list_id', 'key', name='uq_list_column_key')
    )
    op.create_index('idx_columns_list', 'columns', ['list_id'])

    # Create items table
    op.create_table('items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('list_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=True),
        sa.Column('updated_by', sa.UUID(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('archived_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_items_list', 'items', ['list_id'])
    op.create_index('idx_items_list_updated', 'items', ['list_id', sa.text('updated_at DESC')])
    op.execute('CREATE INDEX idx_items_values_gin ON items USING GIN (values)')


def downgrade() -> None:
    op.drop_index('idx_items_values_gin', table_name='items')
    op.drop_index('idx_items_list_updated', table_name='items')
    op.drop_index('idx_items_list', table_name='items')
    op.drop_table('items')
    
    op.drop_index('idx_columns_list', table_name='columns')
    op.drop_table('columns')
    
    op.drop_index('idx_lists_workspace_archived', table_name='lists')
    op.drop_index('idx_lists_workspace', table_name='lists')
    op.drop_table('lists')
