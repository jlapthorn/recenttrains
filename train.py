#!/usr/env/python
import requests
from pushbullet import Pushbullet
from bs4 import BeautifulSoup

#How many minutes late before delay repay
late=0
#URL used to scrap recenttraintimes.co.uk
url="http://www.recenttraintimes.co.uk/Home/Search?Op=Srch&Fr=Winnersh+%28WNS%29&To=London+Waterloo+%28WAT%29&TimTyp=D&TimDay=4a&Days=Wk&TimPer=4w&dtFr=&dtTo=&ShwTim=AvAr&TOC=All&ArrSta=5&MetAvg=Mea&MetSpr=RT&MxScDu=&MxSvAg=&MnScCt=&MxArCl=5"

def pushbulletinit(msg):
    pb = Pushbullet("o.5V4FfVDdrdhvDsuxFH0Hmt7M5enT5bAq")
    push = pb.push_note("SWR Late Trains Alert", msg)

r = requests.get(url) # Get The URL
soup = BeautifulSoup(r.text, 'lxml') # Parse the HTML as a string
trainTimes = soup.find_all('table')[1] # Find the second table containing train times

for table_row in trainTimes.select("tr"):
    cells = table_row.findAll('td')
    if len(cells) > 0 and len(cells[6]) > 0:
        leave=cells[1].text.strip()
        arrival=cells[2].text.strip()
        time,status=cells[6].text.strip().split(" ")
        if "L" in status: 
            minutes=int(status.replace('L',''))
            if minutes > late:
                msg = "The train leaving Winnersh at {0} was more than {3} minutes late.  It was {1} minutes late in total arriving at {2}".format(leave, str(minutes),arrival,str(late))   
                pushbulletinit(msg)

