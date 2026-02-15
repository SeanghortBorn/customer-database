"""Add relationships comments and audit

Revision ID: 3f4g5h6i7j8k
Revises: 2a3b4c5d6e7f
Create Date: 2026-02-15 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3f4g5h6i7j8k'
down_revision: Union[str, None] = '2a3b4c5d6e7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for relationship_type if it does not exist.
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'relationship_type') THEN
                CREATE TYPE relationship_type AS ENUM ('one_to_many', 'many_to_many');
            END IF;
        END$$;
        """
    )
    
    # Create relationships table
    op.create_table('relationships',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('list_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('target_list_id', sa.UUID(), nullable=False),
        sa.Column('relationship_type', sa.Enum('one_to_many', 'many_to_many', name='relationship_type'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['list_id'], ['lists.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_list_id'], ['lists.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_relationships_list', 'relationships', ['list_id'])
    op.create_index('idx_relationships_target', 'relationships', ['target_list_id'])

    # Create relationship_links table
    op.create_table('relationship_links',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('relationship_id', sa.UUID(), nullable=False),
        sa.Column('source_item_id', sa.UUID(), nullable=False),
        sa.Column('target_item_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['relationship_id'], ['relationships.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_item_id'], ['items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_item_id'], ['items.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('relationship_id', 'source_item_id', 'target_item_id', name='uq_relationship_link')
    )
    op.create_index('idx_rel_links_relationship', 'relationship_links', ['relationship_id'])
    op.create_index('idx_rel_links_source', 'relationship_links', ['source_item_id'])
    op.create_index('idx_rel_links_target', 'relationship_links', ['target_item_id'])

    # Create comments table
    op.create_table('comments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('item_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_comments_item', 'comments', ['item_id'])
    op.create_index('idx_comments_user', 'comments', ['user_id'])

    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('workspace_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('action', sa.Text(), nullable=False),
        sa.Column('entity_type', sa.Text(), nullable=True),
        sa.Column('entity_id', sa.UUID(), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_workspace', 'audit_logs', ['workspace_id'])
    op.create_index('idx_audit_user', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_entity', 'audit_logs', ['entity_type', 'entity_id'])
    op.create_index('idx_audit_created', 'audit_logs', [sa.text('created_at DESC')])


def downgrade() -> None:
    op.drop_index('idx_audit_created', table_name='audit_logs')
    op.drop_index('idx_audit_entity', table_name='audit_logs')
    op.drop_index('idx_audit_user', table_name='audit_logs')
    op.drop_index('idx_audit_workspace', table_name='audit_logs')
    op.drop_table('audit_logs')
    
    op.drop_index('idx_comments_user', table_name='comments')
    op.drop_index('idx_comments_item', table_name='comments')
    op.drop_table('comments')
    
    op.drop_index('idx_rel_links_target', table_name='relationship_links')
    op.drop_index('idx_rel_links_source', table_name='relationship_links')
    op.drop_index('idx_rel_links_relationship', table_name='relationship_links')
    op.drop_table('relationship_links')
    
    op.drop_index('idx_relationships_target', table_name='relationships')
    op.drop_index('idx_relationships_list', table_name='relationships')
    op.drop_table('relationships')
    
    op.execute("DROP TYPE IF EXISTS relationship_type")
