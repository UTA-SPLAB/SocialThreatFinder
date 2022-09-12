# Using Twarc2 to collect phishing reports

import time
import os
from drivers.time_sensitive import *


def collect_tweets():

	timestamp=fetch_time()

	#timestamp=timestamp+25200 # Comment out to catch up with UTC time. 25200 value for PST (California) time. Change value accordingly.

	query_time=timestamp-1200 # Only get tweets from 20 mins before.
	query_time_dt=convert_epoch_to_datetime(query_time)

	import twarc

	os.system(f'twarc2 search --archive --start-time "{query_time_dt}" --limit 100 "hxxps" raw_output/phishing_hxxps.jsonl')
	os.system("twarc2 csv raw_output/phishing_hxxps.jsonl raw_output/phishing_hxxps.csv")










