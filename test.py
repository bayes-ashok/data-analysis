from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/namibia-vs-sri-lanka-1st-match-first-round-group-a-1298135/full-scorecard")

# Allow time for JavaScript to load the content
time.sleep(5)  # Adjust delay if necessary

# Get the page source after rendering
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Find all tables with the specified class
tables = soup.find_all("table", class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")

if tables:
    for idx, table in enumerate(tables, start=1):
        # Open a CSV file to save data for each table
        csv_filename = f"table_{idx}.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Extract rows
            rows = table.find_all("tr")
            for row in rows:
                # Extract columns
                columns = row.find_all(["td", "th"])
                data = [col.text.strip() for col in columns]
                
                # Only write the row if it has 8 values
                if len(data) == 8:
                    csvwriter.writerow(data)
        
        print(f"Table {idx} saved to {csv_filename}")
else:
    print("No tables found.")

# Close the browser
driver.quit()
