import requests,time,smtplib, lxml
from bs4 import BeautifulSoup
from notify_run import Notify
from datetime import datetime
import re

'''

IN ORDER TO USE WITH GMAIL, MAKE SURE THAT YOU HAVE "LESS SECURE" EMAILS TO BE TURNED ON IN ORDER TO
BE ABLE TO SEND EMAILS

'''
url = "https://www.amazon.com/Western-Digital-Elements-Portable-External/dp/B06W55K9N6/ref=sr_1_3?crid=2EB6J15NDL34C&keywords=hard+drive&qid=1570609209&s=electronics&sprefix=hard+%2Celectronics%2C204&sr=1-3"
desiredPrice = 80

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 \
    Safari/537.36',
    }
def checkPrice():
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find("span", id = "productTitle").text
        price = soup.find("span", {"id": "priceblock_ourprice"}).text

        trim = re.compile(r'[^\d.,]+')
        mainPrice = trim.sub('', price)
        priceNow = float(mainPrice)
        
  #VARIABLES FOR SENDING MAIL ---------------------------------------
        title1=str(title.strip())
        print("NAME : "+ title1)
        print("CURRENT PRICE : " + "$" + str(priceNow))
        print("DESIRED PRICE : " + "$" + str(desiredPrice))

  #FUNCTION TO CHECK THE PRICE-------------------------------------------------------
 
        count = 0
        if(priceNow <= desiredPrice):
                sendMail(title)
                
                
        else:
                count = count+1
                print("Rechecking... Last checked at "+str(datetime.now()))
 
#Lets send the mail-----------------------------------------------------------------
def sendMail(title):


        server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('you@gmail.com','yourPassword')
	subject = "Price of " + str(title.strip()) + " " + " has fallen below $" + str(desiredPrice)
	body = "Hey YOU! \n The price of "+ str(title.strip()) + " has fallen below $"+  str(desiredPrice)+".\n So, hurry up & check the amazon link right now : "+url
	msg = "Subject: {} \n\n {} ".format(subject,body)
	
	server.sendmail(
	'you@gmail.com','to@email.com',msg)
	print("EMAIL HAS BEEN SENT SUCCESSFULLY.")
	server.quit()


print("Check again after an hour.")
count = 0

while(True):
	count += 1
	print("Check : "+str(count))
	checkPrice()
	time.sleep(3600)

