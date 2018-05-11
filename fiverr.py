import re
import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from emailx import get_email
town_list = []
with open('town.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
town_list = [x.strip() for x in content] 

service_list = []
with open('services.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
service_list = [x.strip() for x in content] 

current_dir = os.path.dirname(os.path.abspath(__file__)) 
val = str(current_dir) + "\chromedriver"
browser = webdriver.Chrome(str(val))
# print(service_list)
# print(town_list)
for service in service_list:
	for town in town_list:
		search_term = str(service) + " " + str(town)
		f = open(search_term,"w+")
		browser.get('https://www.google.co.in/search?q=&npsic=0&rflfq=1&rlha=0&rllag=51136382,869325,1970&tbm=lcl&ved=0ahUKEwjHk7T1lvTZAhVHYo8KHU1GAUgQjGoIaQ&tbs=lrf:!2m1!1e3!3sIAE,lf:1,lf_ui:2&rldoc=1#rlfi=hd:;si:;mv:!1m3!1d17051.630571922742!2d0.87223795!3d51.14550385!2m3!1f0!2f0!3f0!3m2!1i381!2i327!4f13.1;tbs:lrf:!2m1!1e3!3sIAE,lf:1,lf_ui:2')
		s_b = browser.find_element_by_id('lst-ib')
		browser.execute_script('arguments[0].innerHTML = "";',s_b)	
		s_b.send_keys("")
		s_b.send_keys(search_term)
		s_b.send_keys(Keys.ENTER)
		website = browser.find_elements_by_xpath("//a[@class='yYlJEf L48Cpd']")
		if(website):
			for e in website:
				emails = []
				url = e.get_attribute('href')
				emails = get_email(url)
				if emails:
					for email in emails:
						print(email)
						f.write(email + "\n")
			f.close()
			print('---------------\n')



