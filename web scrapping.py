
#######################################################################################
###############################Extracting Main Table#################################
#######################################################################################

import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=89"

# Sending an HTTP request to the URL
response = requests.get(url)

# Parsing the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Extracting the table by class name
table = soup.find("table", class_="ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide")

# Save the data to a CSV file
csv_filename = "t20_world_cup_2024_results_with_links.csv"

if table:
    rows = table.find_all("tr")
    
    # Open a CSV file for writing
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Iterate through rows and write to the CSV
        for row in rows:
            columns = row.find_all(["th", "td"])
            row_data = []
            
            for col in columns:
                # Check if the column contains an <a> tag
                link = col.find("a")
                if link and link.has_attr("href"):
                    # Append the hyperlink instead of the text
                    row_data.append(link["href"])

                else:
                    # Append the plain text
                    row_data.append(col.text.strip())
            
            writer.writerow(row_data)
    
    print(f"Table data with links has been saved to {csv_filename}")
else:
    print("Table not found")

