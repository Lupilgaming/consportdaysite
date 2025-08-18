from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time 
import os
import csv 

def filter_csv_by_unique_column(input_filepath, output_filepath, column_index):
    seen_values = set()
    filtered_rows = []
    with open(input_filepath, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        # header = next(reader)  # Read the header row # no header
        #filtered_rows.append(header)
        for row in reader:
            if len(row) > column_index:  # Ensure the column exists in the row
                column_value = row[column_index]
                if column_value not in seen_values:
                    seen_values.add(column_value)
                    filtered_rows.append(row)
    with open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(filtered_rows)

def dumpactivities(atheleteid, weeks, fileout):
    activities = []
    for week in weeks:
        try:
            #print(f"running for {atheleteid}, {week}")
            linktogetfrom = f"https://www.strava.com/athletes/{atheleteid}#interval?interval={week}&interval_type=week&chart_type=miles&year_offset=0"
            driver.get(linktogetfrom)
            # scroll to end
            last_height = driver.execute_script("return document.body.scrollHeight")
            #print(last_height)
            for i in range(25):
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1300);")
                # Wait for new content to load
                time.sleep(2)
                # Calculate new scroll height and compare with last
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    #print("End of page reached. at ", i)
                    break
                last_height = new_height
            # lets iterate over all activities in this week 
            pattern = re.compile(r'https://www.strava.com/activities/')
            web_feed_entries = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='web-feed-entry']")
            for w in web_feed_entries:
                # get all the links in this 
                links = w.find_elements(By.TAG_NAME, "a")
                hrefs = [link.get_attribute("href") for link in links]
                activhref = [href for href in hrefs if pattern.search(href)]
                activities = activities + activhref
            activities = [x for x in activities if not x.__contains__('best')]
            activities = [x for x in activities if not x.__contains__('segments')]
            activities = [x for x in activities if not x.__contains__('traini')]
        except Exception as e:
            print(f"error occured at {atheleteid}, {week}: {e}")
            continue
    activities = [x+'\n' for x in activities]
    with open(fileout, 'a', encoding='utf-8') as fw:
        fw.writelines(activities)
    filter_csv_by_unique_column(fileout, fileout, 0)

with open('out.csv', 'r', encoding='utf-8') as fr:
    data = fr.readlines()

# data contains <link> , <atheletename>
# we only use link  

atheletes = [x.split(',')[0].split('/')[-1] for x in data]
atheletes = [x for x in atheletes if not x.__contains__('log')]

#weeks     = ['202529', '202530', '202531', '202532', '202533']
weeks     = ['202530', '202531', '202532', '202533']                               ## add your custom weeks here 

skipit = True
from tqdm import tqdm
pbar = tqdm(total=len(atheletes), desc="Processing Items")
for athelete in atheletes:
    if athelete == atheletes[0]:
        skipit = False
    if skipit:
        continue
    else:
        dumpactivities(athelete, weeks, os.path.join('tempdump', f"f{athelete}.dmp"))
        pbar.update(1)
pbar.close()
