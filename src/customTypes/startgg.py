from typing import TypedDict

# region SuccessResponse


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
    events: list["Event"]


class Event(TypedDict):
    name: str


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
