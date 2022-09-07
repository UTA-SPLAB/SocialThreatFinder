# Using Twarc2 to collect phishing reports

import time
import os

def collect_tweets():

	import twarc

	os.system('twarc2 search --archive --limit 100 "hxxps" raw_output/phishing_hxxps.jsonl')
	os.system("twarc2 csv raw_output/phishing_hxxps.jsonl raw_output/phishing_hxxps.csv")













