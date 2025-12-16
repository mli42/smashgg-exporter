import argparse
import csv
import datetime
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import DATE, cast, select
from sqlalchemy.orm import joinedload, raiseload

from main import load_database
from models import EventDB, SetDB, TournamentDB
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
            cast(EventDB.start_at, DATE) >= date.fromtimestamp(args.startDate),
            cast(EventDB.start_at, DATE) <= date.fromtimestamp(args.endDate),
        )
        .options(
            joinedload(SetDB.event).joinedload(EventDB.tournament),
            joinedload(SetDB.winner_player),
            joinedload(SetDB.loser_player),
            raiseload("*")
        )
    )

    if args.countryCode:
        stmt = stmt.where(TournamentDB.country_code == args.countryCode)
    if args.addrState:
        stmt = stmt.where(TournamentDB.addr_state == args.addrState)

    fetch_time_start = datetime.datetime.now()
    sets = session.scalars(stmt).all()
    fetch_time_end = datetime.datetime.now()
    delta_time = fetch_time_end - fetch_time_start

    session.close()

    print(f"> Fetched {len(sets)} sets, delta time: {delta_time}")
    return sets


def main(args: argparse.Namespace):
    sets = fetch_sets(args)

    now_timestamp = datetime.datetime.now().timestamp()
    output_filename = f"{now_timestamp}-{args.outSuffix}.csv" if args.outSuffix else f"{now_timestamp}.csv"
    output_path = f"output/{output_filename}"

    with open(output_path, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

        wr.writerow([
            'set_id',
            'event_date',
            'tournament',
            'event'
            'event_entrants',
            'winner',
            'loser',
            'winner_seed',
            'loser_seed',
            'winner_score',
            'loser_score',
        ])

        for set_db in sets:
            wr.writerow([
                set_db.id,
                set_db.event.start_at.replace(tzinfo=datetime.timezone.utc),
                f"{set_db.event.tournament.name} ({set_db.event.tournament.id})",
                f"{set_db.event.name} ({set_db.event.id})",
                set_db.event.num_entrants,
                f"{set_db.winner_player.gamer_tag} ({set_db.winner_player.id})",
                f"{set_db.loser_player.gamer_tag} ({set_db.loser_player.id})",
                set_db.winner_seed,
                set_db.loser_seed,
                set_db.winner_score,
                set_db.loser_score,
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
