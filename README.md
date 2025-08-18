# consportdaysite

The idea is to have a test browser : 
1. Open Strava.com
2. Login manually
3. Adjust strava **club code** in place of clubid in **line13 of postlogin_getlist.py** to **scrape list of members** from strava
4. This generates a file named out.csv containing all athelete links
5. Run **createactivitydump.py** -- to adjust for how many weeks you want the data change the array **line 77/78 {weeks = ['202530', '202531']}**
   a. To get what week id you should use goto athelete page and select the week in chart -- read the url and you will understand (read line31 of the file)
   b. Or based on whatever date range you have get the year (2025) and week number (30) -- most likely how strava names its interval variable
6. Close the browser with driver.exit() and exit()
7. Now we have a **list of acitivities** present in an unique file for each atheleteid inside tempdmp folder
8. Iterate over all the activites and scrape out the data however you want ( for reference use the no_sel.py script)
9. Create a dashboard for however you want ( for reference use showdb.py or this static site )

For how tos on running selenium read docs -- https://selenium-python.readthedocs.io/ or https://www.selenium.dev/documentation/

If you cant read them all just do 3 things (**TLDR**) : (and use the check_selenium.py it will launch a browser window then close it asap dont worry the code only closes it)
1. Download a separate test browser ( better practice as far as i am concerned )
2. Download corresponding driver
3. pip install selenium and boom ready to go ( now i think selenium package downloads and locally caches driver so step 2 might be optional )

If you want **to fasten up the speed** :
1. Use multiple sessions in parallel and selectively scrape pages
   a. It is better practice that if you have n parallel sessions to scrape total k pages then just have each session scrape pages in order - [i,i+n....k] where i is [0...(k mod n)]
2. Download all the activity pages in parallel ( If unix machine then just parallel download with wget -- too bad am on windows :( )
3. Scrape them offline

highest rewarding singular activity events :

<img width="796" height="430" alt="image" src="https://github.com/user-attachments/assets/4b22b040-a003-47d8-b330-650d3ce912a7" />

Scraping indvid. activities : 
![str1](https://github.com/user-attachments/assets/86b7e29f-944d-4f52-a26f-fe1f6ef43472)
