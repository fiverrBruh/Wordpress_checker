from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import re
import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os.path
from wordpress_checker import check
def get_email(urli):
	if(check(urli) == 0):
		return
	current_dir = os.path.dirname(os.path.abspath(__file__)) 
	val = str(current_dir) + "\chromedriver"
	driver = webdriver.Chrome(str(val))
	print("fucking here urli\n "+urli)
	driver.get(str(urli))
	urlInput = urli

	new_urls = deque([urlInput])
	 
	# a set of urls that we have already crawled
	processed_urls = set()
	 
	# a set of crawled emails
	emails = set()

	#opening a new file
	#exiting the program after scannig 100 links
	maxPage = 10
	maxPage = int(maxPage)
	cnt = 0
	# process urls one by one until we exhaust the queue
	while len(new_urls):
	 
	    # move next url from the queue to the set of processed urls
	    url = new_urls.popleft()
	    processed_urls.add(url)

	    if cnt>=maxPage:
	        break
	    else:
	        cnt+=1
	 
	    # extract base url to resolve relative links
	    parts = urlsplit(url)
	    base_url = "{0.scheme}://{0.netloc}".format(parts)
	    path = url[:url.rfind('/')+1] if '/' in parts.path else url
	 
	    # get url's content
	    print("Processing %s" % url)
	    try:
	        response = requests.get(url)
	    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
	        # ignore pages with errors
	        continue
	 
	    # extract all email addresses and add them into the resulting set
	    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
	    emails.update(new_emails)

	    # create a beutiful soup for the html document
	    
	    soup = BeautifulSoup(response.text,"html.parser")
	 
	    # find and process all the anchors in the document
	    for anchor in soup.find_all("a","p","div","span"):
	        # extract link url from the anchor
	        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
	        if(len(link) == 0):
	        	link = anchor.getText()
	        print("link-->" + str(link) + "\n")
	        # resolve relative links
	        if link.startswith('/'):
	            link = base_url + link
	        elif not link.startswith('http'):
	            link = path + link
	        # add the new url to the queue if it was not enqueued nor processed yet
	        if not link in new_urls and not link in processed_urls:
	            new_urls.append(link)

	    driver.quit()
	    #storing emails in a txt file
	    return(emails)
	    