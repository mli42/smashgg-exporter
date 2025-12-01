TOURNAMENTS_QUERY = """
query TournamentsQuery(
  $afterDate: Timestamp,
  $beforeDate: Timestamp,
  $countryCode: String,
  $addrState: String,
  $perPage: Int
) {
  tournaments(
    query: {
      sortBy: "startAt desc",
      perPage: $perPage,
      filter: {
        past: true,
        videogameIds: [1386],
        countryCode: $countryCode,
        addrState: $addrState,
        afterDate: $afterDate,
        beforeDate: $beforeDate
      }
    }
  ) {
    pageInfo {
      total
      totalPages
      page
      perPage
    }
    nodes {
      id
      name
      url
      countryCode
      addrState
      events(filter: {videogameId: [1386]}) {
        name
        videogame {
          id
          name
        }
      }
    }
  }
}
"""
