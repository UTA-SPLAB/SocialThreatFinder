import re
import pandas as pd

def format_url(tweet_text):
      regex_hxxp = 'hxxp[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
      urls = []
      processed_url = 'Null'
      y = 'Null'

        # if("hxxp" or "hxxps" in full_text):

        # it will return list of all urls found by REGEX.
      urls.append(re.findall(regex_hxxp, tweet_text))


      for y in urls[0]:
       
          # logic here is every hxxps has hxxp but hxxp does not have hxxps.
          # so look for hxxps first, then hxxp.
          if('hxxp' in y.lower()):
              final_url = y.replace("[.]", ".").replace("hxxp", "http")
              processed_url = final_url.lower()
              return processed_url


def process():
      df=pd.read_csv("raw_data/phishing_hxxps.csv")


      for index, row in df.iterrows():
            tweet_id=(row['id'])
            tweet_text=(row['tweet'])
            creation_date=(row['date'])
            creation_time=(row['time'])
            image_url=(row['thumbnail'])
            processed_url=format_url(tweet_text)




            print(tweet_id)
            print(tweet_text)
            print(creation_date)
            print(creation_time)
            print(image_url)
            print(processed_url)

process()

