import requests
from bs4 import BeautifulSoup

# URL of the match overs comparison page
url = "https://www.espncricinfo.com/records/year/team-highest-innings-totals/2023-2023/list-a-matches-5"

# Team name to filter for (case insensitive)
team_to_find = "India".lower()  # Convert to lowercase

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables on the page
    tables = soup.find_all('table')
    
    # Flag to check if at least one table is found
    table_found = False
    
    # Iterate through each table
    for table in tables:
        # Process each row in the table
        rows = table.find_all('tr')
        
        # Skip the first row (header row)
        for row in rows[1:]:
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract data from specific cells
            row_data = [
                cells[0].get_text(strip=True),   # 1st cell
                cells[1].get_text(strip=True),   # 2nd cell
                cells[5].get_text(strip=True),   # 6th cell
                cells[6].get_text(strip=True),   # 7th cell
                cells[7].get_text(strip=True)    # 8th cell
            ]
            
            # Check if the first cell contains the desired team name (case insensitive)
            if row_data[0].lower() == team_to_find:
                # Print the selected cells of the row_data
                print(row_data)
                table_found = True
            
        if table_found:
            break  # Stop searching through tables once we found and printed the desired team's data
    
    if not table_found:
        print(f"No data found for '{team_to_find}' in the tables on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
