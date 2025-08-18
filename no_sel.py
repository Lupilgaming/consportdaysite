from bs4 import BeautifulSoup
#import html2text
import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time




BASE_URL = "http://www.strava.com/athletes/"

def createlocalsoup(filename):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup

def make_soup(url):
    # soup = BeautifulSoup(browser.open(url).read())
    # return soup
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def getactivitydetails(act_link):
    soup = make_soup(act_link)
    # Example: Extracting activity title
    activity_name = soup.select('span[class*="Summary_typeText"]')[0].get_text().strip()
    doa           = soup.select('time[class*="Summary_date"]')[0].get('datetime').strip()
    athelete_name = soup.select('[class*="AthleteBanner_name" i]')[0].get_text().strip()
    # dont take athelete id as people share activities
    # get three labels -- distance time elevation -- Stat_statLabel
    labels        = soup.select('span[class*="Stat_statLabel"]')
    values        = soup.select('[class*="Stat_statValu"]') 
    distance = "none"
    duration = "none"
    # skip elevation
    for i, l in enumerate(labels) : 
        if l.get_text().strip().lower().__contains__("distance"):
            distance = values[i].get_text().strip()
        if l.get_text().strip().lower().__contains__("time"):
            duration = values[i].get_text().strip()
    finalout = f"{activity_name},{doa},{distance},{duration}"
    #print(finalout)
    return finalout


outfile = "tempdmp.csv"

pbar = tqdm(total=1621, desc="Processing Items")

skipit = True
i = 0
for filename in os.listdir('tempdump'):
    fname = os.path.join('tempdump', filename)
    aid   = filename[1:-4]
    print(f"adding details for {aid}")
    dat   = []
    fw = open(outfile, 'a', encoding='utf-8')
    with open(fname, 'r', encoding='utf-8') as fr:
        data = fr.readlines()
    for link in data :
        i = i+1
        if i == 1582:
            skipit = False
        if skipit: 
            pbar.update(1)
            continue
        link = link.strip()
        if len(link) < 5:
            continue
        det = getactivitydetails(link)
        pbar.update(1)
        det = f"{aid},{det}\n"
        fw.write(det)
        dat.append(det)
    fw.close()
pbar.close()


##  adding links (activity links )
outfile = "tempdmp.csv"

pbar = tqdm(total=1621, desc="Processing Items")

with open(outfile, 'r', encoding='utf-8') as fr:
    odata = fr.readlines()
i = 0
for filename in os.listdir('tempdump'):
    fname = os.path.join('tempdump', filename)
    aid   = filename[1:-4]
    #print(f"adding details for {aid}")
    dat   = []
    with open(fname, 'r', encoding='utf-8') as fr:
        data = fr.readlines()
    for link in data :
        link = link.strip()
        if len(link) < 5:
            continue
        pbar.update(1)
        odata[i] = odata[i][:-1]+f",{link}\n"
        i = i+1
with open(outfile+"d", 'w' , encoding='utf-8') as fw:
    fw.writelines(odata)

pbar.close()

### adding names 
with open("out.csv", 'r', encoding='utf-8') as fr:
   data = fr.readlines()
at = [x.split(',')[0].split('/')[-1] for x in data]
nam = [x.split(',')[1].strip()  for x in data ]
mappin =  {at[i]: nam[i] for i in range(len(at))}


with open('tempdmp.csvd', 'r', encoding='utf-8') as fr:
    data = fr.readlines()
for i,line in enumerate(data):
    data[i] = data[i][:-1]+f",{mappin[line.split(',')[0].strip()]}\n" 
with open('tempdmp.csvde', 'w', encoding='utf-8') as fw:
    fw.writelines(data)
