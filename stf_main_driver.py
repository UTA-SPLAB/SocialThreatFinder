# Social ThreatFinder main driver

# python3 run_stf.py to start the program


from drivers.crawl import collect_tweets # Tweet crawling module
from drivers.url_activity import url_activity_check
from drivers.domain_info import registrar_info
#from drivers.vt import vtscan
from drivers.countdown_timer import countdown
#from drivers.html_table_generator import htg # Removed from open-source release 0.19 onwards. 
from drivers.screenshot import take_screenshot
from drivers.get_place import country_city
# from drivers.populate import * # Contains populate_from_database and build_map functions. For fetching data from database and populating the map. Removed from open-source release 0.19 onwards.
#from drivers.front_end import create_frontend # Generate front-end UI. Removed from open source release 0.19 onwards.
from drivers.find_phish_target import find_phish_target # Get the targetted organization of the tweet
from drivers.hideOutput import blockPrint,enablePrint # Module to hide stdout console output

# ML-models

from drivers.predict_url_activity import check_if_active_ml # CNN model to check if URL is active


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

def database_handler(tweet_id,processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target,ml_phish_verdict_text):
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
        headers=['Tweet_id','URL','registrar_name','ip_address','URL is alive','Geo co-ordinates','Location','Creation_time','image_url','Target','ML_verdict(Experimental)']
        fields=[tweet_id,processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target,ml_phish_verdict_text]
        with open(r'database/db_unsorted.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(fields)
            print("Database updated")


def database_sorter():
    db_frame = pd.read_csv('database/db_unsorted.csv') 
    db_frame = db_frame.drop_duplicates(subset='URL', keep="first")
    db_frame.to_csv('database/db.csv')
    print("Database sorted")
    #print(db_frame)

def capture_ip(url):

    socket.setdefaulttimeout(20)

    try:


        domain = urlparse(str(url)).netloc
        print(domain) # --> www.example.test

     
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
                    print("Process:Get geo-location of IP")
                    new_cords = get_geo(ip_address)
                    try:
                        with time_limit(10):
                            print("Check if URL is active")
                            url_activity=url_activity_check(final_url)
                    except TimeoutException as e:
                        print("Timed out!")
                    
                    print("Process:Get registrar name")
                    registrar_name=registrar_info(final_url)
                    #print("Process:VirusTotal")
                    #detections=vtscan(tweet_id,final_url) # Removed VirusTotal from production version 0.13. 
                    try:
                        place=country_city(new_cords[0],new_cords[1])
                    except:
                        place='Unknown' # Invalid co-ords. Possible geoip issue or IP address not resolved
                    
                    #target=fetch_target(hashtags) # Depriciated in 0.17 due to target being identifiable from tweet text itself


                    print("Process: Find targetted organization")
                    target=find_phish_target(tweet_text)
                    if target==None:
                        target="Unknown"


                    print("Process: Get image of the URL for ML verdict")
                    take_screenshot(tweet_id,final_url)
                    print("Taken screenshot, sleeping")
                    
                    # EXPERIMENTAL FEATURE == CNN classifier to predict if the website is phishing
                    # This is an early model, and will be improved upon on subsequent iterations

                    print("Process: Predict if URL is active")
                    
                    try:
                        ml_phish_verdict=check_if_active_ml(f"{tweet_id}.png")
                        if ml_phish_verdict==1:
                            ml_phish_verdict_text="Active phish"
                            print(f"Website {tweet_id} is phishing.")
                        elif ml_phish_verdict==0:
                            print(f"Website {tweet_id} is benign.")
                            ml_phish_verdict_text="Benign/Inactive"
                        
                    except Exception as e:
                        print(e)
                        print(f"Unexpected error for Website {tweet_id}") # This will occur when image is not present
                        ml_phish_verdict_text="Unknown"


                    database_handler(tweet_id, processed_url,registrar_name,ip_address,url_activity,new_cords,place,creation_date,image_url,target,ml_phish_verdict_text)
                 

                except Exception as e: 
                    print(e)
            else:
                print("Tweet already seen, skipping")

   

def run_iteration():
    collect_tweets('lite','hxxps') # Mode= 1) default for full archive (Twitter Academic access key needed), and 2) lite for regular Twitter API tweets. See drivers/crawl.py for more info.
    process('phishing_hxxps')
    collect_tweets('lite','hxxp')
    process('phishing_hxxp')
    


