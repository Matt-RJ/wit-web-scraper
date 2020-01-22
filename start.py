#! /usr/bin/env python3

import requests
import urllib.request
from bs4 import BeautifulSoup
import time
from time import gmtime, strftime
import os

# Url of page to scrape
url = "https://studentssp.wit.ie/LOGIN/?APP=OLEXAMRESULT"

# The text that appears while the results are not up yet
textToSearch = "Semester One Exam results will be released on Wednesday 22nd January at 12.30 pm"

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    print("Starting web scraper...")
    while True:
        print('\x1b[2K\r', end='')
        scrape()

        countdown = 30
        while (countdown > 0):
            countdown -= 1
            time.sleep(1)
            print('\x1b[2K\r' + str(countdown) + ' seconds until next check', end='')

def scrape():
    res = requests.get(url)
    if (res.status_code < 200 or res.status_code > 299):
        print(f"There was an error from the url given (status code {res.status_code})")
        exit(1)
    
    soup = BeautifulSoup(res.text, "html.parser")
    foundText = soup.findAll(text=textToSearch)
    if (foundText):
        print('\n' + color.FAIL + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\t\tThe results are not up yet." + color.ENDC)
    else:
        print('\n' + color.BOLD + color.OKGREEN + 
        strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\t\tThe results are up." + color.ENDC)
        notify('WIT','The WIT results are now live')
        exit(0)

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

if (__name__ == "__main__"):
    """ Executed when run from the command line """
    main()