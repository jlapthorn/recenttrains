#!/usr/env/python
import requests
import time
from bs4 import BeautifulSoup
from common import *
import datetime
import telegram


#How many minutes late before delay repay
late=lateTime
#URL used to scrap recenttraintimes.co.uk
midday=datetime.time(pmHour)
now=datetime.datetime.now()
if now.hour < midday.hour:
    url=amURL
else:
    url=pmURL

if debug: print url

def telegramMessage(msg):
  bot=telegram.Bot(token=telegramToken)
  chat_id = bot.get_updates()[-1].message.chat_id
  bot.send_message(chat_id, text=msg)

def main():
    r = requests.get(url) # Get The URL
    soup = BeautifulSoup(r.text, 'html.parser') # Parse the HTML as a string
    trainTimes = soup.find_all('table')[1] # Find the second table containing train times

    for table_row in trainTimes.select("tr"):
        cells = table_row.findAll('td')
	#print len(cells[6])
        if len(cells) > 0 and len(cells[6]) > 0 and cells[6].text.strip() != "...":
	    leave=cells[1].text.strip()
            arrival=cells[2].text.strip()
            ttime,status=cells[6].text.strip().split(" ")
            if debug: print leave,arrival,ttime,status
            if "L" in status: 
                minutes=int(status.replace('L',''))
                if debug: print minutes, late
                if minutes > late:
                    msg = "The train leaving Winnersh at {0} was more than {3} minutes late.  It was {1} minutes late in total arriving at {2}".format(leave, str(minutes),arrival,str(late))   
                    telegramMessage(msg)
            elif "CANC" in status:
            	if debug: print status
		msg = "The train leaving Winnersh at {0} was cancelled".format(leave)  
		telegramMessage(msg)




if __name__ == "__main__":
   main()




