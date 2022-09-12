import requests
def url_activity_check(url):
   try:
      response = requests.get(str(url))
      if response.status_code == 200:
          return 1 # 1=Active
      else:
          return 0 # 0 =Inactive
   except:
      return 999 # 999 = Error