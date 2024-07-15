import requests
from bs4 import BeautifulSoup

# URL of the match overs comparison page
url = "https://www.espncricinfo.com/series/zimbabwe-vs-india-2024-1420218/zimbabwe-vs-india-5th-t20i-1420227/match-overs-comparison"

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
        for row in table.find_all('tr'):
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract and print data from each cell
            row_data = [cell.get_text(strip=True) for cell in cells]
            print(row_data)
            
        table_found = True  # Set table_found to True if we found at least one table
    
    if not table_found:
        print("No tables found on the page. Check the webpage structure.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
