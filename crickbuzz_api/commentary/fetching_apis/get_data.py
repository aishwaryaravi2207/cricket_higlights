import requests
import json
from concurrent.futures import ThreadPoolExecutor

# series id - 5945 obtained from (https://cricbuzz-cricket.p.rapidapi.com/series/v1/archives/international?year=2023)

# get matches from series

headers = {
    "X-RapidAPI-Key": "634498eb5dmshda362836424c154p198681jsn8b8da8426658",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
}


def get_matches(series_id):
    response = requests.get(
        f"""https://cricbuzz-cricket.p.rapidapi.com/series/v1/{series_id}""",
        headers=headers,
    )
    matches = response.json()
    print(matches)
    with open("matches.json", "w") as f:
        f.write(json.dumps(matches))
        f.close()


def get_match_ids():
    match_ids = []
    f = open("matches.json", "r")
    match_data = json.loads(f.read())
    for match_detail in match_data["matchDetails"]:
        match_detail_map = match_detail.get("matchDetailsMap", None)
        if match_detail_map:
            for match in match_detail_map["match"]:
                match_ids.append(match["matchInfo"]["matchId"])
    f.close()
    return match_ids


# uses the cricbuzz api instead of rapid api
def get_commentary(match_id):
    commentary_data = []
    response = requests.get(
        f"""https://www.cricbuzz.com/api/cricket-match/commentary/{match_id}""",
    )
    data = response.json()
    commentary_data = commentary_data + data["commentaryList"]
    commentary_data = commentary_data + get_recursive_commentary(
        match_id,
        data["commentaryList"][-1]["timestamp"],
        data["commentaryList"][-1]["inningsId"],
        commentary_data,
    )
    with open(f"commentary/comm_data/{match_id}.json", "w") as f:
        f.write(json.dumps(commentary_data))
        f.close()


# gets the commentary recursively
def get_recursive_commentary(match_id, timestamp, innings_id, commentary_data):
    response = requests.get(
        f"""https://www.cricbuzz.com/api/cricket-match/commentary-pagination/{match_id}/{innings_id}/{timestamp}""",
    )
    data = response.json()
    commentary_data = commentary_data + data["commentaryList"]
    if data["commentaryList"][-1].get("inningsId", None):
        return get_recursive_commentary(
            match_id,
            data["commentaryList"][-1]["timestamp"],
            data["commentaryList"][-1].get("inningsId", 1),
            commentary_data,
        )
    else:
        return commentary_data


def main():
    # get the matches and stores in the file
    # get_matches(5945)

    # gets the match ids from the file generated in previous step
    match_ids = get_match_ids()

    # uses threading to get the commentary data for 10 matches at a time
    with ThreadPoolExecutor(10) as executor:
        executor.map(get_commentary, match_ids)


if __name__ == "__main__":
    main()
