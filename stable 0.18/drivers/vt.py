from virustotal_python import VirustotalError
from pprint import pprint
from base64 import urlsafe_b64encode
import hashlib

# Source - https://github.com/dbrennand/virustotal-python

from virustotal_python import Virustotal

def vtscan(tweetid,url):
# v2 example
    vtotal = Virustotal(API_KEY="aeaa9656525c9a1b99a3f8a4754457beb784b39e0aeb87ef24b6b79613d03339")

    # v2 example
    try:
        # Send a URL to VirusTotal for analysis
        resp = vtotal.request("url/scan", params={"url": url}, method="POST")
        url_resp = resp.json()
        # Obtain scan_id
        scan_id = url_resp["scan_id"]
        # Request report for URL analysis
        analysis_resp = vtotal.request("url/report", params={"resource": scan_id})
        #print(analysis_resp.response_code)
        a=analysis_resp.json()
        file=open("log/vt/"+str(tweetid)+".json","w")
        file.write(str(a))
        file.close()
        #print(a)
        try:
            detections=a['positives']
            return detections
        except: # URL has not yet been scanned
            detections=0
            return detections
    except VirustotalError as err:
        return 999
 
