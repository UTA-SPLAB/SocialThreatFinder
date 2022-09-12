import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os


def take_screenshot(url_id,url): # URL ID == Tweet_id
 
	print(url_id)
	if 'http' not in url:
		url='http://'+url
	

	options = webdriver.ChromeOptions()
	options.headless = True
	driver = webdriver.Chrome(options=options)
	#driver = webdriver.Chrome(executable_path='/home/delphinus/Desktop/chromedriver/chromedriver',options=options)

	driver.get(url)

	time.sleep(3)

	driver.save_screenshot(f'screens/{url_id}.png')

	driver.quit()

# Test

#take_screenshot('12345','http://www.google.com')
