import argparse
import csv
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import DATE, cast, select
from sqlalchemy.orm import joinedload, raiseload

from main import load_database
from models import EventDB, SetDB, TeamDB, TournamentDB
from utils.getDateTimestamp import get_date_timestamp
from utils.parse_str_or_none import parse_str_or_none


def fetch_sets(args: argparse.Namespace):
    load_dotenv()
    session = load_database()

    stmt = (
        select(SetDB)
        .join(EventDB)
        .join(TournamentDB)
        .where(
            cast(EventDB.start_at, DATE) >= datetime.fromtimestamp(
                args.startDate,
                tz=timezone.utc
            ),
            cast(EventDB.start_at, DATE) <= datetime.fromtimestamp(
                args.endDate,
                tz=timezone.utc
            ),
        )
        .options(
            joinedload(SetDB.event).joinedload(EventDB.tournament),
            joinedload(SetDB.winner_team).joinedload(TeamDB.players),
            joinedload(SetDB.loser_team).joinedload(TeamDB.players),
            raiseload("*")
        )
    )

    if args.countryCode:
        stmt = stmt.where(TournamentDB.country_code == args.countryCode)
    if args.addrState:
        stmt = stmt.where(TournamentDB.addr_state == args.addrState)

    fetch_time_start = datetime.now()
    sets = session.scalars(stmt).unique().all()
    fetch_time_end = datetime.now()
    delta_time = fetch_time_end - fetch_time_start

    session.close()

    print(f"> Fetched {len(sets)} sets, delta time: {delta_time}")
    return sets


def main(args: argparse.Namespace):
    sets = fetch_sets(args)

    now_timestamp = datetime.now().timestamp()
    output_filename = f"{now_timestamp}-{args.outSuffix}.csv" if args.outSuffix else f"{now_timestamp}.csv"
    output_path = f"output/{output_filename}"

    max_players_count = max([
        max(
            len(set_db.winner_team.players),
            len(set_db.loser_team.players),
        ) for set_db in sets
    ])

    with open(output_path, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        wr.writerow([
            'set_id',
            'event_date',
            'tournament',
            'event'
            'event_entrants',
            *[f"winner_{i+1}" for i in range(max_players_count)],
            *[f"loser_{i+1}" for i in range(max_players_count)],
            'winner_seed',
            'loser_seed',
            'winner_score',
            'loser_score',
            'winner_team_players_count',
            'loser_team_players_count',
        ])

        for set_db in sets:
            winner_team_players_count = len(set_db.winner_team.players)
            loser_team_players_count = len(set_db.loser_team.players)

            padWinnerPlayers = (
                [None] * (max_players_count - winner_team_players_count)
            )
            padLoserPlayers = (
                [None] * (max_players_count - loser_team_players_count)
            )

            wr.writerow([
                set_db.id,
                set_db.event.start_at,
                f"{set_db.event.tournament.name} ({set_db.event.tournament.id})",
                f"{set_db.event.name} ({set_db.event.id})",
                set_db.event.num_entrants,
                *[
                    f"{winner_player.gamer_tag} ({winner_player.id})"
                    for winner_player in set_db.winner_team.players
                ],
                *padWinnerPlayers,
                *[
                    f"{loser_player.gamer_tag} ({loser_player.id})"
                    for loser_player in set_db.loser_team.players
                ],
                *padLoserPlayers,
                set_db.winner_seed,
                set_db.loser_seed,
                set_db.winner_score,
                set_db.loser_score,
                winner_team_players_count,
                loser_team_players_count,
            ])
    print(f"> Exported data to {output_path}")


def load_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fetches sets from database and saves them in a local csv'
    )

    parser.add_argument(
        '--startDate',
        action='store',
        default=get_date_timestamp("01-01-2025"),
        type=lambda s: get_date_timestamp(s),
        help='fetch from startDate DD-MM-YYYY (default: 01-01-2025)'
    )
    parser.add_argument(
        '--endDate',
        action='store',
        default=get_date_timestamp("01-04-2025"),
        type=lambda s: get_date_timestamp(s),
        help='fetch up to endDate DD-MM-YYYY (default: 01-04-2025)'
    )
    parser.add_argument(
        '--countryCode',
        action='store',
        default="FR",
        type=parse_str_or_none,
        help='CountryCode of the tournament, can be set to `None` (default: FR)'
    )
    parser.add_argument(
        '--addrState',
        action='store',
        default="IDF",
        type=parse_str_or_none,
        help='AddrState of the tournament, can be set to `None` (default: IDF)'
    )
    parser.add_argument(
        '--outSuffix',
        action='store',
        default=None,
        type=str,
        help='csv output filename to `output/{timestamp}-{outSuffix}.csv` (default: `output/{timestamp}.csv`)'
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = load_args()

    main(args)
