'''
Created on Feb 13, 2019

@author: Neil
'''

import imaplib
import email


user = 'capstonespamtest@gmail.com'
password = 'BigMike1'
imap_url = 'imap.gmail.com'

con = imaplib.IMAP4_SSL(imap_url)  # initialize connection

con.login(user, password)  # login

# print (con.list())  # show all folders

# pick inbox; returns size (how many emails) (in byte form?)
con.select('INBOX')

# 2 is the index of email in inbox. RFC822 is some specific protocol to get absolutely all the data
# result, data = con.fetch('2', '(RFC822)')
#
# print (result)
# print (data)

# instead of RFC822, you can fetch individual fields:
_, sender = con.fetch('2', '(BODY[HEADER.FIELDS (FROM)])')
_, subject = con.fetch('2', '(BODY[HEADER.FIELDS (SUBJECT)])')

# includes attributes about the text
_, body = con.fetch('2', '(UID BODY[TEXT])')

print(sender[0][1])
print(subject[0][1])
print (body[0][1])
