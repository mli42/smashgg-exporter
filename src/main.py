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
from utils.shouldSkipEvent import should_skip_event


class Player(TypedDict):
    id: int
    gamer_tag: str
    seed: int
    score: int


def get_player_db(player: Player, session: Session) -> PlayerDB:
    saved_player_db = (
        session
        .execute(
            select(PlayerDB).where(PlayerDB.id == player['id'])
        )
        .scalar()
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
        saved_set_db = (
            session
            .execute(
                select(SetDB).where(SetDB.id == event_set['id'])
            )
            .scalar()
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


def main(session: Session):
    afterDate = get_date_timestamp("01/01/2025")
    beforeDate = get_date_timestamp("01/04/2025")

    for tournament in get_tournaments_iter(afterDate, beforeDate):
        saved_tournament = (
            session
            .execute(
                select(TournamentDB).where(TournamentDB.id == tournament.id)
            )
            .scalar()
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


if __name__ == '__main__':
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    def signal_handler(sig, frame):
        print(' Saving before exiting...')
        session.commit()
        session.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    main(session)

    session.commit()
    session.close()
