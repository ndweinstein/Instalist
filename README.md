# Instalist
An Instagram based wordlist generator
This program, given a non-private Instagram username, will scrape that users instagram for words in the posts original comments, as well as hashtags. If a depth greater than 0 is specified, it will recurse down that many layers, each time going through every user that commented on any of the original users posts. I do not reccomend scraping a higher depth than 1. This program is slow.

I take no responsibility for what you do with this program.

#### Install:
  This program requirese selenium, and phantomJS. They can be installed with pip.  
  pip install selenium  
  pip install phantomJS

#### Usage:
  Instalist [-h] [-d DEPTH] [-m MIN] [-p PICTURES] [--version] User

##### positional arguments:
User - An Instagram username

##### optional arguments:
-h, --help  
&nbsp;&nbsp;show this help message and exit  
-d DEPTH, --depth DEPTH  
&nbsp;&nbsp;If specified, other users who have commented on specified users pictures will be scraped as well (recurse up to depth N)  
-m MIN, --min MIN  
&nbsp;&nbsp;Minimum word length to capture (default: 2)  
-p PICTURES, --pictures PICTURES  
&nbsp;&nbsp;If a recursed user has over this many pictures it will skip them (default: 200)  
--version  
&nbsp;&nbsp;Displays version information  
