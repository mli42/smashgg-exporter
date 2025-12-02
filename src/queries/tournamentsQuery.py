TOURNAMENTS_QUERY = """
query TournamentsQuery(
  $afterDate: Timestamp,
  $beforeDate: Timestamp,
  $countryCode: String,
  $addrState: String,
  $perPage: Int,
  $page: Int
) {
  tournaments(
    query: {
      sortBy: "startAt asc",
      perPage: $perPage,
      page: $page,
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
      url(relative: false, tab: "details")
      city
      countryCode
      addrState
      events(filter: {videogameId: [1386], published: true}) {
        id
        name
        numEntrants
        slug
        startAt
        state
        videogame {
          id
          name
        }
      }
    }
  }
}
"""
