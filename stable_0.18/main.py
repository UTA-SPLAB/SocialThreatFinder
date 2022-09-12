
# v0.18

# Fixed bug where app crashed for malformed image urls

# crawl.py now fetches tweets appearing only in last 10 mins to ensure API calls are not wasted.

# Note time is set to UTC by default. Adjust according to your timezone.

# V0.17
  
# Introducing the ThreatFinder REST API! 
# Fetch reports as json, currently supports only GET requests 
# Location: /api/stf_api.py

# Fixed API error when parsing registrar name with non-english characters.


# V0.16

 # Fixed URL rendering bug for reports containing both URL and IP
 # Media attachment json handled in a seperate temp file under raw_output

# V0.15
    # Major: Validity of the phishing report now verified using a CNN image based model
    # under /ml_models/image_based
# v0.14

    # Tesseract model identifies phishing URLs from images.
    # Fix column grid space in database template to prevent overflow of long URLs

# V0.13 Re-integrating Twarc2!
# NLTK to identify targetted organizations from tweet text
# Only 36 brands now, we need to add more!
# V0.12 Now checks for both http and https URLs!
# V0.11 Huge changes!
'''
> Minor: db.csv now sorted to show newer posts at the top, and also get rid of duplicate URL entries.
database_sorter handles this.
> The map is now populated by accessing the database.
This means the model does not start from the beginning on every run. It looks for a database and adds more to it.
The drivers.populate file handles taking data from db.csv. 
> Generating the message for the folium markers is handled by drivers.populate as well
generate_map function shifted to drivers.populate as well.
> This file now mostly handles collecting the data and running the drivers. Let's see if I
can just make this call the drivers and put everything under drivers. Modularity yo!
'''
# V0.10 Gets location country state city from drivers/get_place
# V0.09 Store data into a csv file and create html database
'''
= Stores all info into a database file under /database/db.csv
= Creates a html database table under /templates/database.html which can be visited from dash.html
  driver used /drivers/html_table_generator.py
'''

# V0.08 Added a module for collecting news (depriciated in favor of Twitter embedded widget)
'''
Now embedding the map in another webpage (dash.html) by using iframe. iframe also displays the Twitter embedded widget for news.
Added new module drivers.front_end (Depreciated). It is replaced by the static webpage dash.html which renders map.html as an iframe.
Flask now renders dash.html as well as map.html (as an iframe).
NOTE: Module for collecting news and for rendering front-end are not being used in the final code. 
'''

# V0.07 - Added VirusTotal logging under ../log/vt/ folder
# V0.06 - cumulatively marking pointers.
# Stores dictionaries in ../raw_output/ folder 
''' Custom drivers hosted under .../drivers/
'''
from drivers.crawl import collect_tweets # Tweet crawling module
from drivers.url_activity import url_activity_check
from drivers.domain_info import registrar_info
#from drivers.vt import vtscan
from drivers.countdown_timer import countdown
from drivers.html_table_generator import htg
from drivers.screenshot import take_screenshot
from drivers.get_place import country_city
from drivers.populate import * # Contains populate_from_database and build_map functions. For fetching data from database and populating the map
#from drivers.front_end import create_frontend
from drivers.find_phish_target import find_phish_target # Get the targetted organization of the tweet

# ML-models

#from ml_models.image_based.individual import check_if_phish # CNN ML model to check if website is phish
#from ml_models.tesseract.identify_text import identify_text_from_image # Identify URLs from images using Tesseract


''' 3rd party/native libraries 
'''

import folium
import webbrowser
import time
from folium.plugins import *
import pandas as pd
import whois
import os
import random 
import re
import time
import requests
import json
import socket
from urllib.parse import urlparse
from os.path import exists as file_exists
import csv   
import string 

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

global seen_ids
seen_ids=[] # Twitter ids stored in this list to avoid duplicate URLs in db.
global seen_news_id
seen_news_ids=[]

def remove_files():
    try:
        os.system("rm raw_output/phishing_hxxp.csv")
        os.system("rm raw_output/phishing_hxxps.csv")
    except:
        pass
def urlchecker(url):
   
   w = whois.whois(url)
   print(w)
   time.sleep(5)

def database_handler(tweet_id,processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target):
    check_if_db_file_exists=file_exists('database/db_unsorted.csv')
    if not registrar_name:
        registrar_name='Private'
    if(check_if_db_file_exists==True):

        fields=[tweet_id,processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target]
        with open(r'database/db_unsorted.csv', 'a') as f:

            writer = csv.writer(f)
            writer.writerow(fields)
            print("Database updated")
            # Sorting the database by date so the newer entries come first.

    else:
        headers=['Tweet_id','URL','registrar_name','ip_address','URL is alive','Geo co-ordinates','Location','Creation_time','image_url','Target']
        fields=[tweet_id,processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target]
        with open(r'database/db_unsorted.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(fields)
            print("Database updated")


def database_sorter():
    db_frame = pd.read_csv('database/db_unsorted.csv') 
    # db_frame[pd.to_datetime(db_frame['Creation_time'], errors='coerce').notnull()] # Removing non-numeric rows i.e. getting rid of malformed URL entries.
    # db_frame.sort_values(by='Creation_time')
    db_frame = db_frame.drop_duplicates(subset='URL', keep="first")
    db_frame.to_csv('database/db.csv')
    print("Database sorted")
    #print(db_frame)

def capture_ip(url):

    socket.setdefaulttimeout(20)

    try:


        domain = urlparse(str(url)).netloc
        print(domain) # --> www.example.test

        # IP address to test
        #ip_address = '147.229.2.90'

        # URL to send the request to

        ip_address=socket.gethostbyname(domain)

        return ip_address
    except:
        print("Skipped")

def get_geo(ip_address):


    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    # Send request and decode the result
    response = requests.get(request_url)
    result = response.content.decode()
    # Clean the returned string so it just contains the dictionary data for the IP address
    result = result.split("(")[1].strip(")")
    # Convert this data into a dictionary
    result = json.loads(result)
    coords = []
    latitude = result['latitude']
    longitude = result['longitude']
    coords.append(latitude)
    coords.append(longitude)
    return latitude, longitude


def format_url(tweet_text):
      print(tweet_text.replace("\n","")) # Remove new-line chars in tweet text 
      regex_hxxp = 'hxxp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      urls = []
      processed_url = 'Null'
      y = 'Null'

        # if("hxxp" or "hxxps" in full_text):

        # it will return list of all urls found by REGEX.
      urls.append(re.findall(regex_hxxp, tweet_text))

      print(urls)
      time.sleep(10)


      for y in urls[0]:
       
          # logic here is every hxxps has hxxp but hxxp does not have hxxps.
          # so look for hxxps first, then hxxp.
          if('hxxp' in y.lower()):
              final_url = y.replace("[.]", ".").replace("hxxp", "http")
              processed_url = final_url.lower()
              
              processed_url_sanitized=processed_url.split("\\n")
              processed_url_sanitized=processed_url_sanitized[0].split("\n")

              # print("========== DEBUG ==========")
              print(processed_url_sanitized)
              print(processed_url_sanitized[0])
      
              return processed_url_sanitized[0]
         

def process(filename):
      df=pd.read_csv("raw_output/"+str(filename)+".csv")

      with open('raw_output/seen_url_ids.txt') as f:
        seen_ids_list=[line.rstrip('\n') for line in f]



      start = time.time()
      for index, row in df.iterrows():
            if (time.time() - start) > 20:
                break

            tweet_id=(row['id'])
            print(f"Tweet id:{tweet_id}")
            tweet_text=(row['text'])
            creation_date=(row['created_at'])   ### This section needs changes as Twitter API does not provide date and time.
            creation_time=(row['created_at'])
            #hashtags=(row['hashtags'])
            time_string='<h4><br><font color="MediumVioletRed">Discovered on:'+str(creation_date)+","+str(creation_time)+'</font><br></h4>'
            try:
                image_url_raw=(row['attachments.media']) # Need to fix this field.
                file=open("raw_output/img_temp.json","w")    # Really weird approach to parse json string from a new plain-text file
                file.write(str(image_url_raw))               # NEEDS OPTIMIZATION!
                file.close()
                f=open("raw_output/img_temp.json")
                image_url_json=json.load(f)
                image_url=image_url_json[0]['url'] 
                print(image_url)
                processed_url=format_url(tweet_text)

                # Phase: If URL not found in tweet, we need to check if URL is embedded in an image
            except Exception as e:
                print(e) # Invoked when no embedded image in tweets.
                print("No valid Image URL found")
                processed_url="None"
                image_url="None"

            # ================= ADD: Part to verify if URL is active using ML ===================

            
            # tweet_image=take_screenshot(tweet_id,image_url)
            # phish_url_from_img=identify_text_from_image(tweet_image)
            # if phish_url_from_img==None:
            #     break # Break out of the loop for this particular tweet
            # else:
            #     processed_url=phish_url_from_img


            final_url=processed_url
          
            if str(tweet_id) not in seen_ids_list:

        #print("Tweet id:"+str(tweet_id)+" already used before, ignoring")
    
                file=open("raw_output/seen_url_ids.txt","a")
                file.write(str(tweet_id))
                file.write("\n")

                try:
                    try:
                        with time_limit(10):
                            print("Process:IP")
                            ip_address = capture_ip(final_url)
                    except TimeoutException as e:
                        print("Timed out!")
                    print("Process:GEO")
                    new_cords = get_geo(ip_address)
                    try:
                        with time_limit(10):
                            print("URL activity")
                            url_activity=url_activity_check(final_url)
                    except TimeoutException as e:
                        print("Timed out!")
                    
                    print("Process:Registrar")
                    registrar_name=registrar_info(final_url)
                    #print("Process:VirusTotal")
                    #detections=vtscan(tweet_id,final_url) # Removed VirusTotal from production version 0.13. 
                    try:
                        place=country_city(new_cords[0],new_cords[1])
                    except:
                        place='Unknown' # Invalid co-ords. Possible geoip issue or IP address not resolved
                    #target=fetch_target(hashtags)

                    # print("Process:Screenshot")
                    # image_name=take_screenshot(final_url)

                    print("Process: Find targetted organization")
                    target=find_phish_target(tweet_text)
                    if target==None:
                        target="Unknown"
                    

                    # print("Process: Verify true positive")
                    # check_true_positive=check_if_phish(image_name)
                    # if check==1:

                    database_handler(tweet_id, processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target)
                    # else:
                    #     print(f"URL reported by tweet id:{tweet_id} was a FP, skipping")
                    #     # Note: Alternatively, we can also store this URL to figure out what % of URLs reported are false positives

                except Exception as e: 
                    print(e)
            else:
                print("Tweet already seen, skipping")

   

def steps_hxxps():
    collect_tweets()
    process('phishing_hxxps')
    


def main(): # Runs all the modules in order
    
    print("Refreshing feed")
    remove_files()
    steps_hxxps()
    #steps_hxxp()
    database_sorter()
    #populate_from_database()
    #htg()
    countdown(600) # Wait for 10 mins before starting next iteration
        

main()
