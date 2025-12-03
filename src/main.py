import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import EventDB, TournamentDB
from queries.sets.getSets import get_event_sets_iter
from queries.tournaments.getTournaments import get_tournaments_iter
from utils.constants import STARTGG_BASE_URL
from utils.getDateTimestamp import get_date_timestamp
from utils.shouldSkipEvent import should_skip_event


def handle_event(event: EventDB):
    print(f"EVENT [{event.id}] : {STARTGG_BASE_URL}/{event.slug}")

    for event_set in get_event_sets_iter(event.id):
        player1 = {
            'user_id': event_set['slots'][0]['entrant']['participants'][0]['player']['id'],
            'gamer_tag': event_set['slots'][0]['entrant']['participants'][0]['player']['gamerTag'],
            'seed': event_set['slots'][0]['entrant']['initialSeedNum'],
            'score': event_set['slots'][0]['standing']['stats']['score']['value'] or 0,
        }

        player2 = {
            'user_id': event_set['slots'][1]['entrant']['participants'][0]['player']['id'],
            'gamer_tag': event_set['slots'][1]['entrant']['participants'][0]['player']['gamerTag'],
            'seed': event_set['slots'][1]['entrant']['initialSeedNum'],
            'score': event_set['slots'][1]['standing']['stats']['score']['value'] or 0,
        }

        winnerPlayer, loserPlayer = (
            player1, player2
        ) if player1['score'] > player2['score'] else (
            player2, player1
        )

        print(
            f"{winnerPlayer['gamer_tag']} [{winnerPlayer['score']}] - {loserPlayer['gamer_tag']} [{loserPlayer['score']}]"
        )


def handle_tournament(tournament: TournamentDB):
    for event in tournament.events:

        if should_skip_event(event):
            # event_slug = event['slug'].split('/')[-1]
            # print(f"SKIPPING EVENT : {event_slug} ({event['id']})")
            continue

        handle_event(event)


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

        handle_tournament(tournament)


if __name__ == '__main__':
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is missing")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    main(session)

    session.commit()
    session.close()
