import requests
from bs4 import BeautifulSoup

# URL of the match overs comparison page
url = "https://www.espncricinfo.com/series/major-league-cricket-2024-1432722/seattle-orcas-vs-san-francisco-unicorns-13th-match-1432738/match-overs-comparison"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables on the page
    tables = soup.find_all('table')
    
    # Variables to store team names and scores
    team1_name = None
    team2_name = None
    team1_scores = []
    team2_scores = []
    
    # Iterate through each table
    for table in tables:
        # Process each row in the table
        rows = table.find_all('tr')
        
        # Check if this table contains team names
        header_row = table.find('tr')
        header_cells = header_row.find_all(['th', 'td'])
        if len(header_cells) >= 3:
            team1_name = header_cells[1].get_text(strip=True)
            team2_name = header_cells[2].get_text(strip=True)
        
        # Print team names first
        print(f"\nTeam 1: {team1_name}")
        print(f"Team 2: {team2_name}")
        print()
        
        # Iterate through each row, skipping the first (header) row
        for row in rows[1:]:  # Take all rows for comparison (first 20 overs)
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract data from specific cells
            over_number = cells[0].get_text(strip=True)  # Extract over number
            
            # Team 1 score details
            team1_score_cell_text = cells[1].get_text(strip=True)
            team1_score = team1_score_cell_text.split('(')[0].strip()  # Extract only score part
            team1_scores.append(team1_score)
            
            # Team 2 score details
            team2_score_cell_text = cells[2].get_text(strip=True)
            team2_score = team2_score_cell_text.split('(')[0].strip()  # Extract only score part
            team2_scores.append(team2_score)
        
        break  # Break after processing the first table

    # Now team1_scores and team2_scores contain the scores for Team 1 and Team 2
    print("\nTeam 1 Scores:")
    for over, score in enumerate(team1_scores, start=1):
        print(f"{over}: {score}")
    
    print("\nTeam 2 Scores:")
    for over, score in enumerate(team2_scores, start=1):
        print(f"{over}: {score}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
