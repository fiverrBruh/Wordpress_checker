import re
import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os.path

def check(url):
	current_dir = os.path.dirname(os.path.abspath(__file__)) 
	val = str(current_dir) + "\chromedriver"
	browser = webdriver.Chrome(str(val))
	# url = "http://www.gisidesign.com/"
	checker_url = "https://www.isitwp.com/"
	pstext = "Good news"
	ngtext = "Bad news"
	browser.get(str(checker_url))
	time.sleep(3)
	inp = browser.find_element_by_id('search-input')
	inp.send_keys(str(url))
	btn = browser.find_element_by_id('search-submit')
	btn.click()
	time.sleep(7)
	res_text = browser.find_element_by_class_name('result-content').text
	browser.quit()
	if(pstext in res_text):
		print("it's in wordpress...checking for emails...\n")
		return 1
	else:
		print("its not in wordpress... closing the site.. not checking for emails...\n")
		return 0
	