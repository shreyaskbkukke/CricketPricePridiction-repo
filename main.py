import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the match overs comparison page
url = "https://www.espncricinfo.com/series/zimbabwe-vs-india-2024-1420218/zimbabwe-vs-india-5th-t20i-1420227/match-overs-comparison"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the container that holds the overs comparison data
    tables = soup.find_all('table')
    
    # Define lists to store the data
    over_data = []

    # Process each table to extract data
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols:
                over_data.append(cols)
    
    # Print the extracted data for debugging
    for row in over_data:
        print(row)
    
    # Identify the correct number of columns based on the data
    # Example: If the data has 6 columns, update the DataFrame accordingly
    df = pd.DataFrame(over_data, columns=["Over", "Zimbabwe Runs", "Zimbabwe Wickets", "India Runs", "India Wickets", "Unknown Column"])
    
    # Save the data to a CSV file
    df.to_csv('match_overs_comparison.csv', index=False)
    
    print("Data has been saved to match_overs_comparison.csv")
else:
    print("Failed to retrieve the page")
