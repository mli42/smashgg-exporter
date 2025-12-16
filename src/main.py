import argparse
import os
import signal
import sys
from typing import TypedDict

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from customTypes.startgg import EventSet
from models import EventDB, PlayerDB, SetDB, TournamentDB
from queries.sets.getSets import get_event_sets_iter
from queries.tournaments.getTournaments import get_tournaments_iter
from utils.constants import STARTGG_BASE_URL
from utils.getDateTimestamp import get_date_timestamp
from utils.parse_str_or_none import parse_str_or_none
from utils.shouldSkipEvent import should_skip_event


class Player(TypedDict):
    id: int
    gamer_tag: str
    seed: int
    score: int


def get_player_db(player: Player, session: Session) -> PlayerDB:
    saved_player_db = session.scalar(
        select(PlayerDB).where(PlayerDB.id == player['id'])
    )

    if saved_player_db is None:
        saved_player_db = PlayerDB(
            id=player['id'],
            gamer_tag=player['gamer_tag']
        )
        session.add(saved_player_db)

    return saved_player_db


def handle_set(event_set: EventSet, event: EventDB, session: Session) -> SetDB:
    player1: Player = {
        'id': event_set['slots'][0]['entrant']['participants'][0]['player']['id'],
        'gamer_tag': event_set['slots'][0]['entrant']['participants'][0]['player']['gamerTag'],
        'seed': event_set['slots'][0]['entrant']['initialSeedNum'],
        'score': event_set['slots'][0]['standing']['stats']['score']['value'] or 0,
    }

    player2: Player = {
        'id': event_set['slots'][1]['entrant']['participants'][0]['player']['id'],
        'gamer_tag': event_set['slots'][1]['entrant']['participants'][0]['player']['gamerTag'],
        'seed': event_set['slots'][1]['entrant']['initialSeedNum'],
        'score': event_set['slots'][1]['standing']['stats']['score']['value'] or 0,
    }

    winnerPlayer, loserPlayer = (
        player1, player2
    ) if player1['score'] > player2['score'] else (
        player2, player1
    )

    saved_winner_player_db = get_player_db(winnerPlayer, session)
    saved_loser_player_db = get_player_db(loserPlayer, session)

    saved_set_db = SetDB(
        id=event_set['id'],
        winner_seed=winnerPlayer['seed'],
        loser_seed=loserPlayer['seed'],
        winner_score=winnerPlayer['score'],
        loser_score=loserPlayer['score'],
        winner_player=saved_winner_player_db,
        loser_player=saved_loser_player_db,
        event=event
    )
    session.add(saved_set_db)
    return saved_set_db


def handle_event(event: EventDB, session: Session):
    print(f"EVENT [{event.id}] : {STARTGG_BASE_URL}/{event.slug}")

    set_count = 0
    last_saved_set_count = 0
    for event_set in get_event_sets_iter(event.id):
        saved_set_db = session.scalar(
            select(SetDB).where(SetDB.id == event_set['id'])
        )

        if saved_set_db:
            continue

        handle_set(event_set, event, session)
        set_count += 1

        if (set_count % 25 == 0):
            last_saved_set_count = set_count
            session.commit()

    if (set_count != last_saved_set_count):
        session.commit()


def handle_tournament(tournament: TournamentDB, session: Session):
    for event in tournament.events:

        if should_skip_event(event) or event.imported is True:
            # event_slug = event['slug'].split('/')[-1]
            # print(f"SKIPPING EVENT : {event_slug} ({event['id']})")
            continue

        handle_event(event, session)
        event.imported = True
        session.commit()


def main(session: Session, args: argparse.Namespace):
    tournaments = get_tournaments_iter({
        'afterDate': args.startDate,
        'beforeDate': args.endDate,
        'countryCode': args.countryCode,
        'addrState': args.addrState,
    })

    for tournament in tournaments:
        saved_tournament = session.scalar(
            select(TournamentDB).where(TournamentDB.id == tournament.id)
        )

        if saved_tournament is None:
            saved_tournament = tournament
            session.add(saved_tournament)
            session.commit()

        if (saved_tournament.imported is True):
            continue

        handle_tournament(saved_tournament, session)
        saved_tournament.imported = True
        session.commit()


def load_database(echo=False) -> Session:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing")

    engine = create_engine(DATABASE_URL, echo=echo)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    return session


def load_signal_handler(session: Session):
    def signal_handler(sig, frame):
        print(' Saving before exiting...')
        session.commit()
        session.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


def load_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Fetches sets from start.gg and saves them into a postgres database'
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

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = load_args()
    load_dotenv()
    session = load_database()
    load_signal_handler(session)

    main(session, args)

    session.commit()
    session.close()
