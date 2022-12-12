import sys
import os
import pandas as pd
import difflib

def process(screenshot_file_name):
	orgs=[]

	df=pd.read_csv("drivers/heur_target_finder/orgs_meta.csv")
	for index, row in df.iterrows():
		org=row["name"]
		orgs.append(org)


	#screenshot_file_name = sys.argv[1]
	os.system(f"python3 drivers/heur_target_finder/extract_text_from_image.py {screenshot_file_name}")

	word_list = [] # Words extracted from URL

	with open("drivers/heur_target_finder/temp_text.txt", "r") as f:
		for line in f:
			word_list.extend(line.split())

	word_list = [element.lower() for element in word_list] ; word_list
	for i in word_list:
		if i in orgs:
			return i
			break

def get_target_from_image(url_id,url):

	#print(f"Processing URL:{url_id}")
	target=process(f'screens/{url_id}.png')
	#print(f"URL Target:{target}")
	
	return target



