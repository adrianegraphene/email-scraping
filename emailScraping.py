import imaplib, email
import pandas as pd
from datetime import datetime
from collections import Counter
import getpass

#Authenticate Self
user = "EnterYourGmailAddressHere"
password = getpass.getpass()
imap_url = "imap.gmail.com"

con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)

#Select mailbox
con.select("F5Bot-RoboCalls")

#Select Search Term
result, spam = con.search(None, 'SUBJECT',"robocall")

#Split resultant byteobject 
splitspam = spam[0].split()

#initialize list and counter
spamdatelist = []
i = 0

for num in spam[0].split():
    print("---------------------------")
    print(i)
    if i < 2600: 
        #This lets you skip multiple data points if needed. 2600 is Aug 17th 2020 for "robocalls"
        #4000 is Aug 16h 2020 for "spam"
        i = i +1 
        continue
    #This picks out the date of the each email with the search term above.
    result, email_data = con.uid('fetch', splitspam[i], '(RFC822)')
    raw_email = email_data[0][1].decode("latin-1")
    email_message = email.message_from_string(raw_email)
    #print not needed, but helps to visualize the kind of data being saved. :-5 removes the last 5 chars of nonsense
    print(email_message['Date'][:-5])
    spamdatelist.append(email_message['Date'][:-5])
    i = i+1

#parse through all datelists and count the number of events per day.
event_date_counter = Counter(pd.to_datetime(x).normalize().to_pydatetime() for x in spamdatelist)

#Write out to some excel file through Pandas
pd.DataFrame(event_date_counter, index=[0]).T.to_excel('outputrobocalls.xlsx', header=True, index=True)
#I typically take the xlsx data above and move it into my own plotting software, but there's no reason why you couldn't use
#Python's plotting modulues to do this.
