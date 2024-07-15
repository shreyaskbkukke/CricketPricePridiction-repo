import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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
    
    # List to hold data rows
    all_data_rows = []
    
    # Iterate through each table
    for table in tables:
        # Process each row in the table
        rows = table.find_all('tr')
        
        # Iterate through each row, skipping the first (header) row
        for row in rows[1:]:  # Take all rows for comparison (first 20 overs)
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract data from specific cells
            over_number = int(cells[0].get_text(strip=True))  # Extract over number and convert to integer
            score_cell_text = cells[1].get_text(strip=True)  # Get text from the second cell
            
            # Extract the score before '/' and convert to integer
            score = int(score_cell_text.split('/')[0].strip())
            
            # Append data as a list to all_data_rows
            all_data_rows.append([over_number, score])
            
        table_found = True  # Set table_found to True if we found at least one table
        break  # Break after processing the first table
    
    if not table_found:
        print("No tables found on the page. Check the webpage structure.")
    else:
        # Prepare data for linear regression (first 15 overs)
        data_rows = np.array(all_data_rows[:15])
        X = data_rows[:, 0].reshape(-1, 1)  # Over numbers as independent variable
        y = data_rows[:, 1]  # Scores as dependent variable
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict scores for next 5 overs (over numbers 16 to 20)
        next_five_overs = np.array(range(16, 21)).reshape(-1, 1)
        predicted_scores = model.predict(next_five_overs)
        
        # Print predicted scores for next 5 overs
        print("Predicted Scores for Next 5 Overs:")
        for over, score in zip(next_five_overs.flatten(), predicted_scores):
            print(f"Over {over}: Predicted Score = {score:.2f}")
        
        # Extract actual scores for all 20 overs
        actual_scores = np.array(all_data_rows)[:, 1]
        
        # Plotting actual scores vs predicted scores
        plt.figure(figsize=(10, 6))
        plt.scatter(np.arange(1, 21), actual_scores, color='blue', label='Actual Scores')
        plt.plot(np.concatenate([X.flatten(), next_five_overs.flatten()]), np.concatenate([y, predicted_scores]), color='red', linewidth=2, label='Predicted Scores')
        plt.xlabel('Over Number')
        plt.ylabel('Score')
        plt.title('Actual vs Predicted Scores')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
        # Calculate accuracy metrics
        actual_next_five_scores = actual_scores[15:20]
        rmse = np.sqrt(np.mean((actual_next_five_scores - predicted_scores)**2))
        print(f"Root Mean Squared Error (RMSE) for Predicted Scores: {rmse:.2f}")
        
        # Write all data rows to CSV file for reference
        filename = "cricket_scores.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Over Number', 'Score'])
            writer.writerows(all_data_rows)
        
        print(f"Data successfully written to '{filename}'.")
        
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
