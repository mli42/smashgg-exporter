from typing import TypedDict

from models import ActivityState

# region SuccessTournamentsResponse


class SuccessTournamentsResponse(TypedDict):
    data: "DataTournamentsObject"
    extensions: "ExtensionObject"


class DataTournamentsObject(TypedDict):
    tournaments: "TournamentsObject"


class TournamentsObject(TypedDict):
    pageInfo: "PageInfoObject"
    nodes: list["Tournament"]


class PageInfoObject(TypedDict):
    total: int
    totalPages: int
    page: int
    perPage: int


class Tournament(TypedDict):
    id: int
    name: str
    url: str
    city: str
    countryCode: str
    addrState: str
    events: list["Event"]


class Event(TypedDict):
    id: int
    name: str
    numEntrants: int
    slug: str
    startAt: int
    state: ActivityState


# region SuccessEventSetsResponse


class SuccessEventSetsResponse(TypedDict):
    data: "DataEventSetsObject"
    extensions: "ExtensionObject"


class DataEventSetsObject(TypedDict):
    event: "EventObject"


class EventObject(TypedDict):
    sets: "EventSetsObject"


class EventSetsObject(TypedDict):
    pageInfo: "PageInfoObject"
    nodes: list["EventSet"]


class EventSet(TypedDict):
    id: int
    slots: list["Slot"]


class Slot(TypedDict):
    entrant: "Entrant"
    standing: "Standing"


class Entrant(TypedDict):
    initialSeedNum: int
    participants: list["Participants"]


class Participants(TypedDict):
    player: "Player"


class Player(TypedDict):
    id: int
    gamerTag: str


class Standing(TypedDict):
    stats: "Stats"


class Stats(TypedDict):
    score: "Score"


class Score(TypedDict):
    value: None | int
    """'-1' is DQ, the opponent of a DQ has None"""


class ExtensionObject(TypedDict):
    queryComplexity: int


# region ErrorResponse

class ErrorResponse(TypedDict):
    success: bool
    message: str
    errors: list["GraphQLError"]


class GraphQLError(TypedDict):
    message: str

# endregion


StartggTournamentsResponse = SuccessTournamentsResponse | ErrorResponse

StartggEventSetsResponse = SuccessEventSetsResponse | ErrorResponse
