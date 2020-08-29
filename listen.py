import time
from datetime import date

import requests

BASE_URL = "https://statsapi.mlb.com"
SCHEDULE_URL = BASE_URL + "/api/v1/schedule?sportId=1&hydrate=team,linescore"
TODAY = str(date.today())


def main():

    game_url = get_game_url()
    play_radio = True

    while True:

        current_status = game_in_progress(game_url)

        if current_status != play_radio:
            if play_radio:
                print("muting")
            else:
                print("playing radio")

            play_radio = current_status

        time.sleep(10)


def game_in_progress(game_url):

    r = requests.get(game_url)
    current_play = r.json()["liveData"]["plays"]["currentPlay"]

    return current_play["count"]["outs"] != 3


def get_game_url():

    r = requests.get(SCHEDULE_URL)
    all_dates = r.json()["dates"]
    todays_games = [d["games"] for d in all_dates if d["date"] == TODAY][0]

    game_list = [
        g
        for g in todays_games
        if "Indians"
        in [g["teams"][side]["team"]["teamName"] for side in ("home", "away")]
        and g["status"]["abstractGameState"] == "Live"
    ]

    if not game_list:
        raise ValueError("No Nats game found- are they playing right now?")

    game = game_list[0]

    return BASE_URL + game["link"]


if __name__ == "__main__":
    main()
