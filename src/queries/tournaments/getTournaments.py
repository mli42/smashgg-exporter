import os
from datetime import datetime, timezone
from time import sleep
from typing import Generator, cast

import requests

from customTypes.startgg import (StartggTournamentsResponse,
                                 SuccessTournamentsResponse)
from models import EventDB, TournamentDB
from utils.constants import STARTGG_API_URL

from .tournamentsQuery import TOURNAMENTS_QUERY


def get_tournaments(
    afterDate: int,
    beforeDate: int,
    page: int,
) -> SuccessTournamentsResponse:
    STARTGG_TOKEN = os.getenv('STARTGG_TOKEN')

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {STARTGG_TOKEN}",
    }

    BODY = {
        "query": TOURNAMENTS_QUERY,
        "variables": {
            "afterDate": afterDate,
            "beforeDate": beforeDate,
            "countryCode": "FR",
            "addrState": "IDF",
            "perPage": 5,
            "page": page,
        }
    }

    retries = 1

    for attempt in range(retries):
        if attempt != 0:
            sleep(2)

        try:
            response: StartggTournamentsResponse = requests \
                .post(STARTGG_API_URL, json=BODY, headers=HEADERS) \
                .json()

            if (response.get('success') is False):
                raise Exception(response.get('message'))

            if (response.get('errors') is not None):
                raise Exception(response.get('errors', [])[0]['message'])

            return cast(SuccessTournamentsResponse, response)
        except Exception as e:
            print(f"Error with request. Retrying ({attempt+1}/{retries})...")
            print(f"> {e}")

    raise RuntimeError("Request failed")


def get_tournaments_iter(
    afterDate: int,
    beforeDate: int,
) -> Generator[TournamentDB, None, None]:
    response = get_tournaments(afterDate, beforeDate, 1)
    totalPages = response['data']['tournaments']['pageInfo']['totalPages']

    for page in range(2, totalPages + 2):
        # print(f"{response['extensions']['queryComplexity'] = }")
        pageInfo = response['data']['tournaments']['pageInfo']
        tournaments = response['data']['tournaments']['nodes']

        print(f"> Tournaments {pageInfo = }")

        for tournament in tournaments:
            yield TournamentDB(
                id=tournament['id'],
                name=tournament['name'],
                url=tournament['url'],
                city=tournament['city'],
                country_code=tournament['countryCode'],
                addr_state=tournament['addrState'],
                events=[
                    EventDB(
                        id=event['id'],
                        name=event['name'],
                        num_entrants=event['numEntrants'],
                        slug=event['slug'],
                        start_at=(
                            datetime
                            .fromtimestamp(event['startAt'])
                            .replace(tzinfo=timezone.utc)
                        ),
                        state=event['state'],
                    ) for event in tournament['events']
                ]
            )

        if (page != totalPages + 1):
            response = get_tournaments(afterDate, beforeDate, page)
