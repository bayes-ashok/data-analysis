from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

linkInitial="https://www.espncricinfo.com"
finalLink=""
completeLink=linkInitial+finalLink

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get(completeLink)

# Allow time for JavaScript to load the content
time.sleep(5)  # Adjust delay if necessary

# Get the page source after rendering
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Find all tables with the specified class
tables = soup.find_all("table", class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")

# Open a single CSV file to save data for all tables
csv_filename = "combined_table.csv"
with open(csv_filename, "a", newline="", encoding="utf-8") as csvfile:
    
    csvwriter = csv.writer(csvfile)

    # Check if tables exist
    if tables:
        for idx, table in enumerate(tables, start=1):
            # Extract rows from each table
            rows = table.find_all("tr")
            for row in rows:
                # Extract columns
                columns = row.find_all(["td", "th"])
                data = [col.text.strip() for col in columns]

                # Only write the row if it has 8 values
                if len(data) == 8:
                    csvwriter.writerow(data)
        print(f"All tables combined and saved to {csv_filename}")
    else:
        print("No tables found.")

# Close the browser
driver.quit()
