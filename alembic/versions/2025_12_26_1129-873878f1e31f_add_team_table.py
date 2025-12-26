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

    connection = op.get_bind()
    metadata = sa.MetaData()

    set_table = sa.Table(
        "set",
        metadata,
        sa.Column("id", sa.Integer),
        sa.Column("event_id", sa.Integer),
        sa.Column("winner_player_id", sa.Integer),
        sa.Column("loser_player_id", sa.Integer),
        sa.Column("winner_team_id", sa.Integer),
        sa.Column("loser_team_id", sa.Integer),
    )

    team_table = sa.Table(
        "team",
        metadata,
        sa.Column("id", sa.Integer),
    )

    team_player_table = sa.Table(
        "team_player",
        metadata,
        sa.Column("team_id", sa.Integer),
        sa.Column("player_id", sa.Integer),
    )

    # cache: (event_id, player_id) -> team_id
    team_cache = {}

    rows = connection.execute(
        sa.select(
            set_table.c.id,
            set_table.c.event_id,
            set_table.c.winner_player_id,
            set_table.c.loser_player_id,
        )
    ).fetchall()

    for set_id, event_id, winner_pid, loser_pid in rows:
        for pid in (winner_pid, loser_pid):
            key = (event_id, pid)

            if key not in team_cache:
                team_id = connection.scalar(
                    team_table.insert().returning(team_table.c.id)
                )

                connection.execute(
                    team_player_table.insert().values(
                        team_id=team_id,
                        player_id=pid,
                    )
                )

                team_cache[key] = team_id

        connection.execute(
            set_table.update()
            .where(set_table.c.id == set_id)
            .values(
                winner_team_id=team_cache[(event_id, winner_pid)],
                loser_team_id=team_cache[(event_id, loser_pid)],
            )
        )

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
