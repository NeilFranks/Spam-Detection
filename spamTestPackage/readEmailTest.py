'''
Created on Feb 13, 2019

@author: Neil
'''
import imaplib
import email


class emailLoginInfo:

    def __init__(self, newImapURL, newUsername, newPassword):
        self.imapURL = newImapURL
        self.username = newUsername
        self.password = newPassword


gmail = emailLoginInfo(
    'imap.gmail.com', 'capstonespamtest@gmail.com', 'BigMike1')

outlook = emailLoginInfo(
    'imap-mail.outlook.com', 'capstonespamtest@outlook.com', 'BigMike1')

aol = emailLoginInfo(
    'imap.aol.com', 'capstonespamtest@aol.com', 'BigMike1')

yahoo = emailLoginInfo(
    'imap.mail.yahoo.com', 'capstonespamtest@yahoo.com', 'BigMike1')

auths = [gmail, outlook, aol, yahoo]


for auth in auths:
    con = imaplib.IMAP4_SSL(auth.imapURL)  # initialize connection

    con.login(auth.username, auth.password)  # log in

    # print (con.list())  # show all folders

    # pick inbox; returns size (how many emails) (in byte form?)
    con.select('INBOX')

    # 2 is the index of email in inbox. RFC822 is some specific protocol to get absolutely all the data
    # result, data = con.fetch('2', '(RFC822)')
    # result, data = con.fetch('2', '(BODY[HEADER.FIELDS (FROM)])')
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
