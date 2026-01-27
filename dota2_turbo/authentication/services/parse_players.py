import os
import time
import csv
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


API_DELAY = 1.5


def get_players_from_match(match_id):
    print(f"Getting players out of a match: {match_id}")
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when receiving the match {match_id}")
        return []
    data = response.json()
    players = data.get("players", [])
    return [p.get("account_id") for p in players if p.get("account_id")]


def save_to_csv(account_ids):
    path = r"dota2_turbo\authentication\feeds\users.csv"
    existing_ids = set()
    if os.path.exists(path):
        with open(path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("account_id"):
                    existing_ids.add(int(row["account_id"]))

    all_ids = existing_ids.union(set(account_ids))

    print(f"Total number of unique players: {len(all_ids)}")
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["account_id"])
        for acc_id in sorted(all_ids):
            writer.writerow([acc_id])
    print("Done!")


def get_dotabuff_match_ids_selenium(url, max_matches=100):
    print("Launching the browser to receive match_id...")
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    match_links = soup.select("tbody tr td a[href^='/matches/']")
    match_ids = []
    for link in match_links:
        href = link.get("href")
        if href and "/matches/" in href:
            match_id = href.split("/matches/")[1]
            if match_id.isdigit():
                match_ids.append(int(match_id))
        if len(match_ids) >= max_matches:
            break

    return match_ids


def main():
    dotabuff_url = "https://www.dotabuff.com/matches?game_mode=turbo&region=russia"
    match_ids = get_dotabuff_match_ids_selenium(dotabuff_url, max_matches=120)

    print(f"Matches found: {len(match_ids)}")
    all_players = []

    for match_id in match_ids:
        players = get_players_from_match(match_id)
        all_players.extend(players)
        time.sleep(API_DELAY)

    save_to_csv(all_players)


if __name__ == "__main__":
    main()
