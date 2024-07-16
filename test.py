import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage
url = "https://www.espncricinfo.com/series/lanka-premier-league-2024-1421415/colombo-strikers-vs-galle-marvels-19th-match-1428477/full-scorecard"

# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the specific line containing overs information
    overs_line = soup.find(text=re.compile(r'\(\d+ ov'))

    if overs_line:
        # Use regex to extract the total overs
        match = re.search(r'\((\d+) ov', overs_line)
        if match:
            total_overs = match.group(1)
            print(f"Total overs: {total_overs}")
        else:
            print("Total overs not found.")
    else:
        print("Overs line not found on the webpage.")
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")
