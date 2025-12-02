from typing import Literal, TypedDict

# region SuccessResponse

"""enum ActivityState
CREATED: Activity is created
ACTIVE: Activity is active or in progress
COMPLETED: Activity is done
READY: Activity is ready to be started
INVALID: Activity is invalid
CALLED: Activity, like a set, has been called to start
QUEUED: Activity is queued to run
"""
ActivityState = Literal[
    "CREATED",
    "ACTIVE",
    "COMPLETED",
    "READY",
    "INVALID",
    "CALLED",
    "QUEUED"
]


class SuccessResponse(TypedDict):
    data: "DataObject"
    extensions: "ExtensionObject"


class DataObject(TypedDict):
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


StartggResponse = SuccessResponse | ErrorResponse
