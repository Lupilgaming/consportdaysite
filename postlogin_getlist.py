from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time 

# Assuming the browser is already open and the desired page is loaded                  --- copy code wont run add clubid and make driver before this
# driver = webdriver.Chrome()  # Example initialization, not needed if already open
addlines = []

for i in range(1, 5):
    pagaddr = f"https://www.strava.com/clubs/{clubid}/members?page={i}&page_uses_modern_javascript=true"
    driver.get(pagaddr)
    time.sleep(7)
    # Define the pattern to match (e.g., URLs containing 'example.com')
    pattern = re.compile(r'athletes')  # Adjust this regex pattern as needed
    # Find all anchor elements on the page
    links = driver.find_elements(By.TAG_NAME, "a")
    # Lists to store results
    matched_links = []
    matched_texts = []
    # Iterate through each link
    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip()
        
        # Check if the href matches the pattern
        if href and pattern.search(href):
            matched_links.append(href)
            matched_texts.append(text)
    # Output the results
    for link, text in zip(matched_links, matched_texts):
        print(f"Link: {link} | Text: {text}")   
        if len(text.strip()) > 3:
            addlines.append(f"{link}, {text}")
addlines = [x+"\n" for x in addlines]
outfilename = "out.csv"
with open(outfilename, 'w', encoding="utf-8") as fw:
    fw.writelines(addlines)
