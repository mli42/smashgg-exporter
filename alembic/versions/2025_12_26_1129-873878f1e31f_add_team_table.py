"""add team table

Revision ID: 873878f1e31f
Revises: fe9731c112f0
Create Date: 2025-12-26 11:29:52.317444+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '873878f1e31f'
down_revision: Union[str, Sequence[str], None] = 'fe9731c112f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create new tables
    # a. Create team table
    op.create_table(
        'team',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_id'), 'team', ['id'], unique=False)
    op.add_column(
        'set',
        sa.Column(
            'winner_team_id',
            sa.Integer(),
            nullable=True))
    op.add_column(
        'set',
        sa.Column(
            'loser_team_id',
            sa.Integer(),
            nullable=True))
    op.create_foreign_key(None, 'set', 'team', ['winner_team_id'], ['id'])
    op.create_foreign_key(None, 'set', 'team', ['loser_team_id'], ['id'])
    # b. Create team_player pivot table
    op.create_table(
        'team_player',
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
        sa.PrimaryKeyConstraint('team_id', 'player_id')
    )
    op.create_index(
        op.f('ix_team_player_player_id'),
        'team_player',
        ['player_id'],
        unique=False)
    op.create_index(
        op.f('ix_team_player_team_id'),
        'team_player',
        ['team_id'],
        unique=False)
    # 2. Migrate data

    op.execute("""
        WITH players_per_event AS (
            SELECT DISTINCT
                event_id,
                winner_player_id AS player_id
            FROM "set"
            UNION
            SELECT DISTINCT
                event_id,
                loser_player_id AS player_id
            FROM "set"
        ),
        inserted_teams AS (
            INSERT INTO team DEFAULT VALUES
            SELECT COUNT(*) FROM players_per_event
            RETURNING id
        ),
        numbered_teams AS (
            SELECT
                id AS team_id,
                ROW_NUMBER() OVER (ORDER BY id) AS rn
            FROM inserted_teams
        ),
        numbered_players AS (
            SELECT
                event_id,
                player_id,
                ROW_NUMBER() OVER (ORDER BY event_id, player_id) AS rn
            FROM players_per_event
        )
        INSERT INTO team_player (team_id, player_id)
        SELECT
            nt.team_id,
            np.player_id
        FROM numbered_teams nt
        JOIN numbered_players np
        ON nt.rn = np.rn
    """)

    op.execute("""
        UPDATE "set" s
        SET winner_team_id = tp.team_id
        FROM team_player tp
        JOIN (
            SELECT DISTINCT
                event_id,
                winner_player_id AS player_id
            FROM "set"
        ) p
        ON tp.player_id = p.player_id
        WHERE
            s.event_id = p.event_id
            AND s.winner_player_id = p.player_id
        """)

    op.execute("""
        UPDATE "set" s
        SET loser_team_id = tp.team_id
        FROM team_player tp
        JOIN (
            SELECT DISTINCT
                event_id,
                loser_player_id AS player_id
            FROM "set"
        ) p
        ON tp.player_id = p.player_id
        WHERE
            s.event_id = p.event_id
            AND s.loser_player_id = p.player_id
        """)

    op.alter_column("set", "winner_team_id", nullable=False)
    op.alter_column("set", "loser_team_id", nullable=False)

    # 3. Drop old tables
    op.drop_constraint(
        op.f('set_loser_player_id_fkey'),
        'set',
        type_='foreignkey')
    op.drop_constraint(
        op.f('set_winner_player_id_fkey'),
        'set',
        type_='foreignkey')
    op.drop_column('set', 'loser_player_id')
    op.drop_column('set', 'winner_player_id')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Create old table
    op.add_column(
        'set',
        sa.Column(
            'winner_player_id',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True))
    op.add_column(
        'set',
        sa.Column(
            'loser_player_id',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True))
    op.create_foreign_key(
        op.f('set_winner_player_id_fkey'),
        'set',
        'player',
        ['winner_player_id'],
        ['id'])
    op.create_foreign_key(
        op.f('set_loser_player_id_fkey'),
        'set',
        'player',
        ['loser_player_id'],
        ['id'])

    # 2. Migrate data

    op.execute("""
        UPDATE "set" s
        SET winner_player_id = tp.player_id
        FROM team_player tp
        WHERE tp.team_id = s.winner_team_id
        """)
    op.execute("""
        UPDATE "set" s
        SET loser_player_id = tp.player_id
        FROM team_player tp
        WHERE tp.team_id = s.loser_team_id
        """)

    op.alter_column("set", "winner_player_id", nullable=False)
    op.alter_column("set", "loser_player_id", nullable=False)

    # 3. Drop new tables
    # a. Drop team_player pivot table
    op.drop_index(op.f('ix_team_player_team_id'), table_name='team_player')
    op.drop_index(op.f('ix_team_player_player_id'), table_name='team_player')
    op.drop_table('team_player')
    # b. Drop team table
    op.drop_constraint(
        op.f('set_winner_team_id_fkey'),
        'set',
        type_='foreignkey')
    op.drop_constraint(
        op.f('set_loser_team_id_fkey'),
        'set',
        type_='foreignkey')
    op.drop_column('set', 'loser_team_id')
    op.drop_column('set', 'winner_team_id')
    op.drop_index(op.f('ix_team_id'), table_name='team')
    op.drop_table('team')
