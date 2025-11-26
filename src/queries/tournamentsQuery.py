TOURNAMENTS_QUERY = """
query TournamentsQuery($perPage: Int, $coordinates: String!, $radius: String!) {
  tournaments(
    query: {sortBy: "startAt desc", perPage: $perPage, filter: {location: {distanceFrom: $coordinates, distance: $radius}, past: true, videogameIds: [1386], countryCode: "FR", addrState: "IDF", afterDate: 1735689600, beforeDate: 1743465600}}
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

VARIABLES = """
{
  "perPage": 5,
  "coordinates": "48.853495,2.348391",
  "radius": "5mi"
}
"""
