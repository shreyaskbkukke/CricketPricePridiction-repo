import requests
from bs4 import BeautifulSoup
import re
import time

def construct_match_overs_url(base_url):
    """Constructs the URL for match overs comparison based on base_url."""
    last_slash_index = base_url.rfind('/')
    if last_slash_index != -1:
        base_url = base_url[:last_slash_index]
    return base_url + "/match-overs-comparison"


import re

def extract_total_overs(soup):
    """Extracts the total overs information from the webpage."""
    total_overs = None
    try:
        # Find the element containing the overs information
        overs_line = soup.find(string=re.compile(r'(\d+)/(\d+)\s+ov,'))
        print(overs_line)
        if overs_line:
            # Use regex to extract the total overs
            match = re.search(r'/(\d+) ov', overs_line)
            if match:
                total_overs = match.group(1)
                print(f"Total overs: {total_overs}")
            else:
                print("Total overs not found.")
        else:
            print("Overs line not found on the webpage.")
    except Exception as e:
        print(f"Error extracting total overs: {e}")

    return total_overs

def extract_team_scores(soup):
    """Extracts team names and scores from tables on the webpage."""
    tables = soup.find_all('table')
    team1_name, team2_name = None, None
    team1_scores, team2_scores = [], []
    team1_yet_to_bat_added, team2_yet_to_bat_added = False, False
    
    for table in tables:
        rows = table.find_all('tr')
        header_row = table.find('tr')
        header_cells = header_row.find_all(['th', 'td'])
        
        if len(header_cells) >= 3:
            team1_name = header_cells[1].get_text(strip=True)
            team2_name = header_cells[2].get_text(strip=True)

        for row in rows[1:]:  # Skip header row
            cells = row.find_all(['th', 'td'])
            
            if len(cells) > 1:
                team1_score_cell_text = cells[1].get_text(strip=True)
                team1_score = team1_score_cell_text.split('(')[0].strip()
                team1_scores.append(team1_score)
            elif not team1_yet_to_bat_added:
                team1_scores.append("Yet to bat")
                team1_yet_to_bat_added = True

            if len(cells) > 2:
                team2_score_cell_text = cells[2].get_text(strip=True)
                team2_score = team2_score_cell_text.split('(')[0].strip()
                team2_scores.append(team2_score)
            elif not team2_yet_to_bat_added:
                team2_scores.append("Yet to bat")
                team2_yet_to_bat_added = True

        break  # Process only the first table
    
    return team1_name, team2_name, team1_scores, team2_scores

def print_scores(team_name, scores):
    """Prints the scores of a team, skipping 'Yet to bat' or '-' entries."""
    print(f"\nScore of {team_name}:")
    for over, score in enumerate(scores, start=1):
        if score not in ["Yet to bat", "-"]:
            print(f"{over}: {score}")

base_url = """
        https://www.espncricinfo.com/series/lanka-premier-league-2024-1421415/kandy-falcons-vs-dambulla-sixers-18th-match-1428476/match-overs-comparison

        """

url = construct_match_overs_url(base_url)

prev_total_overs = None
prev_team1_scores = None
prev_team2_scores = None

while True:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        team1_name, team2_name, team1_scores, team2_scores = extract_team_scores(soup)
        print("\nMatch Details Detected\n")

        total_overs = extract_total_overs(soup)

        print(f"\nTeam 1: {team1_name}")
        print(f"Team 2: {team2_name}")

        print_scores(team1_name, team1_scores)
        print_scores(team2_name, team2_scores)
        time.sleep(2)

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        time.sleep(60)

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by the user. Exiting...")
        break
