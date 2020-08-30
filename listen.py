import time
from datetime import date

import requests

import radio

BASE_URL = "https://statsapi.mlb.com"
SCHEDULE_URL = BASE_URL + "/api/v1/schedule?sportId=1&hydrate=team,linescore"
TODAY = str(date.today())


def main():

    game_url = get_game_url()
    game_on = None

    while True:

        current_status = game_in_progress(game_url)

        if current_status != game_on:
            if current_status:
                radio.play(106.7)

            else:
                time.sleep(8)
                radio.play(90.9)

            game_on = current_status
        time.sleep(2)


def game_in_progress(game_url):

    r = requests.get(game_url)
    current_play = r.json()["liveData"]["plays"]["currentPlay"]

    count = current_play["count"]

    return count["outs"] != 3 and sum(count.values()) > 0


def get_game_url():

    r = requests.get(SCHEDULE_URL)
    all_dates = r.json()["dates"]
    todays_games = [d["games"] for d in all_dates if d["date"] == TODAY][0]

    game_list = [
        g
        for g in todays_games
        if "Nationals"
        in [g["teams"][side]["team"]["teamName"] for side in ("home", "away")]
        and g["status"]["abstractGameState"] == "Live"
    ]

    if not game_list:
        raise ValueError("No Nats game found- are they playing right now?")

    game = game_list[0]

    return BASE_URL + game["link"]


if __name__ == "__main__":
    main()
