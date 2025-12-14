import argparse
import datetime
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import DATE, cast, select
from sqlalchemy.orm import joinedload, raiseload

from main import load_database
from models import EventDB, SetDB
from utils.getDateTimestamp import get_date_timestamp


def fetch_sets(args: argparse.Namespace):
    load_dotenv()
    session = load_database()

    fetch_time_start = datetime.datetime.now()
    sets = session.scalars(
        select(SetDB)
        .join(EventDB)
        .filter(
            cast(EventDB.start_at, DATE) >= date.fromtimestamp(args.startDate),
            cast(EventDB.start_at, DATE) <= date.fromtimestamp(args.endDate),
        )
        .options(
            joinedload(SetDB.event).joinedload(EventDB.tournament),
            joinedload(SetDB.winner_player),
            joinedload(SetDB.loser_player),
            raiseload("*")
        )
    ).all()
    fetch_time_end = datetime.datetime.now()
    delta_time = fetch_time_end - fetch_time_start

    session.close()

    print(f"> Fetched {len(sets)} sets, delta time: {delta_time}")
    return sets


def main(args: argparse.Namespace):
    sets = fetch_sets(args)

    for set_db in sets:
        print(f"{set_db.event.tournament.name = }")
        break


def load_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fetches sets from database and saves them in a local csv'
    )

    parser.add_argument(
        '--startDate',
        action='store',
        default=get_date_timestamp("01/01/2025"),
        type=lambda s: get_date_timestamp(s),
        help='fetch from startDate DD/MM/YYYY (default: 01/01/2025)'
    )
    parser.add_argument(
        '--endDate',
        action='store',
        default=get_date_timestamp("01/04/2025"),
        type=lambda s: get_date_timestamp(s),
        help='fetch up to endDate DD/MM/YYYY (default: 01/04/2025)'
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = load_args()

    main(args)
