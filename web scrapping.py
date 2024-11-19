import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450"

# Sending an HTTP request to the URL
response = requests.get(url)

# Parsing the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Extracting the table by class name
table = soup.find("table", class_="ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide")

# Save the data to a CSV file
csv_filename = "t20_world_cup_2022_results.csv"

if table:
    rows = table.find_all("tr")
    
    # Open a CSV file for writing
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Iterate through rows and write to the CSV
        for row in rows:
            columns = row.find_all(["th", "td"])
            writer.writerow([col.text.strip() for col in columns])
    
    print(f"Table data has been saved to {csv_filename}")
else:
    print("Table not found")
