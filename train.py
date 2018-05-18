#!/usr/env/python
import requests
import time
from pushbullet import Pushbullet
from bs4 import BeautifulSoup
from common import *
import datetime

#How many minutes late before delay repay
late=lateTime
#URL used to scrap recenttraintimes.co.uk
midday=datetime.time(12)
now=datetime.datetime.now()
if now.hour < midday.hour:
    url=recenttrainsURL
else:
    url=pmURL

if debug: print url


def pushbulletinit(msg):
    pb = Pushbullet(pbSecret)
    push = pb.push_note("SWR Late Trains Alert", msg)

def main():
    r = requests.get(url) # Get The URL
    soup = BeautifulSoup(r.text, 'html.parser') # Parse the HTML as a string
    trainTimes = soup.find_all('table')[1] # Find the second table containing train times

    for table_row in trainTimes.select("tr"):
        cells = table_row.findAll('td')
        if len(cells) > 0 and len(cells[6]) > 0:
            leave=cells[1].text.strip()
            arrival=cells[2].text.strip()
            ttime,status=cells[6].text.strip().split(" ")
            if debug: print leave,arrival,ttime,status
            if "L" in status: 
                minutes=int(status.replace('L',''))
                if debug: print minutes, late
                if minutes > late:
                    msg = "The train leaving Winnersh at {0} was more than {3} minutes late.  It was {1} minutes late in total arriving at {2}".format(leave, str(minutes),arrival,str(late))   
                    pushbulletinit(msg)
    

if __name__ == "__main__":
   main()




