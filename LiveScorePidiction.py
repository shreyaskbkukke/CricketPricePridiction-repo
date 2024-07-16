import requests
from bs4 import BeautifulSoup
import re

def construct_match_overs_url(base_url):
    """Constructs the URL for match overs comparison based on base_url."""
    last_slash_index = base_url.rfind('/')
    if last_slash_index != -1:
        base_url = base_url[:last_slash_index]
    return base_url + "/match-overs-comparison"

def extract_total_overs(soup):
    """Extracts the total overs information from the webpage."""
    overs_line = soup.find(string=re.compile(r'\(\d+ ov'))
    if overs_line:
        match = re.search(r'\((\d+) ov', overs_line)
        if match:
            total_overs = match.group(1)
            return total_overs
    return None

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
    """Prints the scores of a team."""
    print(f"\nScore of {team_name}:")
    for over, score in enumerate(scores, start=1):
        print(f"{over}: {score}")

try:
    base_url = """
    https://www.espncricinfo.com/series/t20-blast-2024-1410370/kent-vs-glamorgan-south-group-1410481//match-overs-comparison
    
    """

    url = construct_match_overs_url(base_url)

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    total_overs = extract_total_overs(soup)
    if total_overs:
        print("\nMatch Details Detected")
        print(f"Total overs: {total_overs}")
    else:
        print("Total overs not found.")

    team1_name, team2_name, team1_scores, team2_scores = extract_team_scores(soup)

    print(f"\nTeam 1: {team1_name}")
    print(f"Team 2: {team2_name}")

    print_scores(team1_name, team1_scores)
    print_scores(team2_name, team2_scores)

except requests.exceptions.RequestException as e:
    print(f"Failed to retrieve the page: {e}")
