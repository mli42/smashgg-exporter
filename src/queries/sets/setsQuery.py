SETS_QUERY = """
query EventsQuery(
  $eventId: ID,
  $perPage: Int,
  $page: Int
) {
  event(id: $eventId) {
    sets(
      page: $page,
      perPage: $perPage,
      sortType: RECENT,
      filters: {hideEmpty: true}
    ) {
      pageInfo {
        total
        totalPages
        page
        perPage
      }
      nodes {
        id
        slots {
          entrant {
            initialSeedNum
            participants {
              id
              player {
                id
                gamerTag
              }
            }
          }
          standing {
            stats {
              score {
                value
              }
            }
          }
        }
      }
    }
  }
}
"""
