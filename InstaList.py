#!/usr/bin/python
from sys import argv, exit
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re
import argparse
#Parse command line arguments and initialize some variables
parser = argparse.ArgumentParser(prog='Instalist', description='Scrape a non-private users instagram for words.')
parser.add_argument('User', help='An Instagram username')
parser.add_argument('-d', '--depth', default=0, type=int, help='If specified, other users who have commented on specified users pictures will be scraped as well (recurse up to depth N)')
parser.add_argument('-m', '--min', default=2, type=int, help='Minimum word length to capture (default: %(default)s)')
parser.add_argument('-p', '--pictures', default=200, type=int, help='If a recursed user has over this many pictures it will skip them (default: %(default)s)')
parser.add_argument('--version', action='version', version='%(prog)s v0.1', help='Displays version information')
args = parser.parse_args()
inituser = args.User
initdepth = args.depth
MINWORDSIZE = args.min
pictures = args.pictures
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
driver = webdriver.PhantomJS()
driver.set_window_size(1920, 1080)
words = []
allfriends = []
REGEX = re.compile('[^a-zA-Z]')
def scrapeUser(user, depth):
	#Check if user exists
	driver.get("https://www.instagram.com/"+user+"/")
	try:
		driver.find_element_by_xpath("//body[@class=' p-error dialog-404']")
		print bcolors.FAIL + "[ User Not Found: " + user + " ]" + bcolors.ENDC
		return 0
	except NoSuchElementException:
		print bcolors.OKGREEN + "[ Found user: " + user + " ]" + bcolors.ENDC
	#Check if account is private
	try:
		driver.find_element_by_xpath("//h2[text()='This Account is Private']")
		print bcolors.FAIL + '\t' +user + " is private, skipping" + bcolors.ENDC
		return 0
	except NoSuchElementException:
		pass
	#If we have recursed at least once make sure the number of posts is less than the limit
	if depth != initdepth:
		try:
			postNumber = driver.find_element_by_xpath("//body/span/section/main/article/header/section/ul/li[1]/span/span")
			if int(postNumber.text.replace(",","")) > pictures:
				print bcolors.FAIL + '\t' + "Too many posts, skipping" + bcolors.ENDC
				return 0
		except NoSuchElementException:
			print bcolors.FAIL + '\t' + "Couldn't find number of posts?" + bcolors.ENDC
	#Scroll the screen if needed
	try:
		driver.find_element_by_xpath("//a[text()='Load more']").click()
		last_height = driver.execute_script("return document.body.scrollHeight")
		count = 0
		while True:
			print bcolors.OKBLUE + '\t' + "Scrolling" + "."*((count%3)+1) + bcolors.ENDC
			count = count + 1
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(2)
			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height
	except NoSuchElementException:
		print bcolors.OKBLUE + '\t' + "No Need To Scroll" + bcolors.ENDC
	#Identify links to posts
	xpath = "//a[contains(@href, '?taken-by=" + user + "')]"
	try:
	        elements = driver.find_elements_by_xpath(xpath)
	except NoSuchElementException:
	        print bcolors.FAIL + '\t' + "No Images Found!" + bcolors.ENDC
		return 0
	links = []
	for element in elements:
			links.append(element.get_attribute('href'))
	friends = []
	#Open wordlist
	if depth == initdepth:
		wordlist = open(inituser, "w")
	else:
		wordlist = open(inituser, "a")
	#Open each post
	for link in links:
		driver.get(link)
		#Find words for wordlist in post comment
		try:
			for word in driver.find_element_by_xpath("//div/div/article/div/div/ul/li/span/span").text.split(" "):
				word = REGEX.sub('', word)
				if word not in words and len(word) > MINWORDSIZE and word.strip() != "":
					words.append(word)
					wordlist.write(word+"\n")
		except NoSuchElementException:
			pass
		#Find words for wordlist in post hashtags
		try:
                        for element in driver.find_elements_by_xpath("//div/div/article/div/div/ul/li/span/a"):
				word = element.text[1:]
				word = REGEX.sub('', word)
                                if word not in words and len(word) > MINWORDSIZE and word.strip() != "":
					words.append(word)
                                        wordlist.write(word+"\n")
		except NoSuchElementException:
			pass
		#If this is not our last recursion, find friends usernames in comments
		if depth != 0:
			try:
				friendElements = driver.find_elements_by_xpath("//body/span/section/main/div/div/article/div/div/ul/li/a")
				for element in friendElements:
					if element.text not in allfriends and "View all" not in element.text and element.text != user:
						friends.append(element.text)
						allfriends.append(element.text)
			except NoSuchElementException:
				pass
	print bcolors.OKGREEN + '\t' + "Found all words and friends for " + user + bcolors.ENDC
	wordlist.close()
	#If this is not our last recursion, recurse through friends
	if depth != 0:
		if friends:
			for friend in friends:
				scrapeUser(friend, depth-1)
				print bcolors.OKGREEN + '\t' + user + " friends: " + str(friends.index(friend)+1) + "/" + str(len(friends)) + bcolors.ENDC
 		else:
			print bcolors.FAIL + user + " has no friends :(" + bcolors.ENDC
	#If all goes well, print a success
	if depth == initdepth:
		print "Successfully saved wordlist " + inituser
#Run the initial function
scrapeUser(inituser, initdepth)
