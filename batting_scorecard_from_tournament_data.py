import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import time
import os

def getScorecard(link):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.espncricinfo.com"+link)

    # Allow time for JavaScript to load the content
    time.sleep(5)  # Adjust delay if necessary

    # Get the page source after rendering
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find all tables with the specified class
    tables = soup.find_all("table", class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")

    # Define the CSV file name
    csv_filename = "batting_scorecard.csv"
    # Check if the CSV file exists
    file_exists = os.path.exists(csv_filename)

    # Open the CSV file in append mode
    with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Check if it's the first scrape (file doesn't exist or is empty)
        if not file_exists or os.stat(csv_filename).st_size == 0:
            for idx, table in enumerate(tables, start=1):
                rows = table.find_all("tr")
                
                # If it's the first table, include all rows
                if idx == 1:
                    row_range = range(len(rows))  # Include all rows for the first table
                else:
                    row_range = range(1, len(rows))  # Skip the first row for subsequent tables
                
                for row_idx in row_range:
                    row = rows[row_idx]
                    columns = row.find_all(["td", "th"])
                    data = [col.text.strip() for col in columns]
                    
                    if len(data) == 8:
                        csvwriter.writerow(data)
            
            print(f"All tables combined and saved to {csv_filename}")

        else:
            # Subsequent scrapes, skip the first row (column names)
            for idx, table in enumerate(tables, start=1):
                # Extract rows from each table
                rows = table.find_all("tr")
                for i, row in enumerate(rows):
                    # Skip the first row (column names)
                    if i == 0:
                        continue

                    # Extract columns
                    columns = row.find_all(["td", "th"])
                    data = [col.text.strip() for col in columns]

                    # Only write the row if it has 8 values
                    if len(data) == 8:
                        csvwriter.writerow(data)
            print(f"Additional tables combined and saved to {csv_filename}")


    # Close the browser
    driver.quit()

# Read the CSV file
with open('t20_world_cup_2024_results_with_links.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header if present
    next(csv_reader)
    
    # Iterate over each row
    for row in csv_reader:
        # Get the last column (link) in the row
        link = row[-1]
        
        # Pass the link to the process_link function
        getScorecard(link)
