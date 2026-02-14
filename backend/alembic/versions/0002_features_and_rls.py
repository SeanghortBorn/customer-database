"""add teams, invites, link shares, price history, indexes & RLS

Revision ID: 0002_features_and_rls
Revises: 0001_initial
Create Date: 2026-02-14 00:00:00.000001
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '0002_features_and_rls'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # create teams, team_members, invites
    op.create_table(
        'teams',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'team_members',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('team_id', pg.UUID(as_uuid=True), sa.ForeignKey('teams.id'), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'invites',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('org_id', pg.UUID(as_uuid=True), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('token', sa.String(), nullable=False, unique=True),
        sa.Column('accepted_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # add link_token to resource_shares
    op.add_column('resource_shares', sa.Column('link_token', sa.String(), nullable=True))

    # create unit price history
    op.create_table(
        'unit_price_history',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('unit_id', pg.UUID(as_uuid=True), sa.ForeignKey('units.id'), nullable=False),
        sa.Column('price', sa.Numeric(12,2), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('effective_date', sa.DateTime(), nullable=True),
        sa.Column('created_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    # Indexes: GIN on JSONB columns
    op.create_index('ix_people_custom_gin', 'people', ['custom'], postgresql_using='gin')
    op.create_index('ix_properties_amenity_tags_gin', 'properties', ['amenity_tags'], postgresql_using='gin')

    # Enable pg_trgm extension and create trigram index for name search
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    op.create_index('ix_people_name_trgm', 'people', ['first_name', 'last_name'], postgresql_using='gin', postgresql_ops={'first_name': 'gin_trgm_ops', 'last_name': 'gin_trgm_ops'})

    # RLS: use session variable zoneer.org (application must set per-session)
    for tbl in ('people','properties','units','resource_shares','comments','activity_logs'):
        op.execute(f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {tbl}_org_isolation ON {tbl} USING (org_id = current_setting('zoneer.org', true)::uuid) WITH CHECK (org_id = current_setting('zoneer.org', true)::uuid);"
        )


def downgrade():
    for tbl in ('people','properties','units','resource_shares','comments','activity_logs'):
        try:
            op.execute(f"ALTER TABLE {tbl} DISABLE ROW LEVEL SECURITY")
        except Exception:
            pass

    op.drop_index('ix_people_name_trgm', table_name='people')
    op.execute('DROP EXTENSION IF EXISTS pg_trgm')
    op.drop_index('ix_properties_amenity_tags_gin', table_name='properties')
    op.drop_index('ix_people_custom_gin', table_name='people')

    op.drop_table('unit_price_history')
    op.drop_column('resource_shares', 'link_token')
    op.drop_table('invites')
    op.drop_table('team_members')
    op.drop_table('teams')
