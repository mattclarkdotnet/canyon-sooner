import requests
from bs4 import BeautifulSoup as bs
import time, datetime
import re
import smtplib

def send_alert():
    # the default alert process is via gmail SMTP (but this only delivers to gmail addresses)
    # 
    # replace this function with your own alert process
    msg = 'Subject: Canyon Alert - Check website'
    fromaddr = 'user@domain.com'
    toaddrs  = ['user@domain.com']
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("user@domain.com", "password")
    print('From: ' + fromaddr)
    print('To: ' + str(toaddrs))
    print('Message: ' + msg)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
intervalMins = 5    
bikes = [
            { "name": "SLX 8 eTap Stealth",
                "url": "https://www.canyon.com/en-au/road-bikes/aero-bikes/aeroad/cf-slx/aeroad-cf-slx-8-etap/3954.html?dwvar_3954_pv_rahmenfarbe=BK%2FBK",
                "size": "M" },
            { "name": "SLX 8 Di2 Stealth",
                "url": "https://www.canyon.com/en-au/road-bikes/aero-bikes/aeroad/cf-slx/aeroad-cf-slx-8-di2/3955.html?dwvar_3955_pv_rahmenfarbe=BK%2FBK",
                "size": "M" },
        ]

while True:
    try:
        print (datetime.datetime.now())
        for bike in bikes:
            print("  Checking for %s, size %s" % (bike["name"], bike["size"]))
            response = requests.get(bike["url"], headers=headers)
            soup = bs(response.text, "html.parser")
            div = soup.find(class_="productConfiguration__selectVariant js-nonSelectableVariation", attrs={"data-product-size": bike["size"]})
            if div is None:
                raise("Product availability not found")
            else:
                if div.find(string=re.compile("soon")) is None:
                    print("  Bike available!")
                    send_alert()
                    exit()
                else:
                    print("  Still coming soon...")
    except Exception as e:
        print(e)

    print(f"  Rechecking in %s minutes\n" % intervalMins)
    time.sleep(intervalMins * 60)


