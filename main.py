import pysmashgg
from dotenv import load_dotenv
import os


def main():
    STARTGG_TOKEN = os.getenv('STARTGG_TOKEN')

    # The second variable is auto retry
    smash = pysmashgg.SmashGG(STARTGG_TOKEN, True)

    # Show event_id for an event, this is for use in the 'event' commands
    event = smash.tournament_show_event_id(
        'smash-summit-10-online', 'melee-singles'
    )
    print(event)


if __name__ == '__main__':
    load_dotenv()
    main()
