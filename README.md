# Instalist
An Instagram based wordlist generator
This program, given an Instagram username, will scrape that users instagram for words in the posts original comments, as well as hashtags. If a depth greater than 0 is specified, it will recurse down that many layers, each time going through every user that commented on any of the original users posts. I do not reccomend scraping a higher depth than 1. 

I take no responsibility for what you do with this program.

usage: Instalist [-h] [-d DEPTH] [-m MIN] [-p PICTURES] [--version] User

Scrape a non-private users instagram for words.

positional arguments:
  User                  An Instagram username

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        If specified, other users who have commented on
                        specified users pictures will be scraped as well
                        (recurse up to depth N)
  -m MIN, --min MIN     Minimum word length to capture (default: 2)
  -p PICTURES, --pictures PICTURES
                        If a recursed user has over this many pictures it will
                        skip them (default: 200)
  --version             Displays version information
