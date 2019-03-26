import imaplib
import smtplib
import email
import base64
import quopri
import re

"""
METHODS FOR EXTRACTION OF EMAIL DATA (SENDER, SUBJECT, AND BODY SO FAR)

"""
def extractSender(myCon, myId):
    _, raw_sender = myCon.fetch(myId, '(BODY[HEADER.FIELDS (FROM)])')
    raw_sender_string = raw_sender[0][1].decode('utf-8')
    sender = email.message_from_string(raw_sender_string)

    """
    sender is in the format: "From: *sender name* <*sender email address*>"
    """

    return sender.as_string()

"""
This function is to decode subjects with emojis in them
"""
def encoded_words_to_text(encoded_words):
    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    match = re.match(encoded_word_regex, encoded_words)

    if match == None:
        #encoded_words didnt match regular expression; they must already be decoded (didnt have any emojis)
        return encoded_words
    else:
        charset, encoding, encoded_text = match.groups()
        if encoding is 'B':
            byte_string = base64.b64decode(encoded_text)
        elif encoding is 'Q':
            byte_string = quopri.decodestring(encoded_text)
        return byte_string.decode(charset)

def extractSubject(myCon, myId):
    _, raw_subject = myCon.fetch(myId, '(BODY[HEADER.FIELDS (SUBJECT)])')
    raw_subject_string = raw_subject[0][1].decode('utf-8')
    encodedSubject = raw_subject_string[9:]  #removing preceding "Subject: "
    subject = "Subject: "+ encoded_words_to_text(encodedSubject) #add preceding subject back on after its been decoded

    """
    subject is in the format: "Subject: *Subject*"
    """

    return subject

def extractBody(myCon, myId):
        _, data = myCon.uid('fetch', myId, '(RFC822)')  # get that email

        # get email into byte literal
        raw_email = data[0][1]
        # NOTE: At this point, Emojis are in UTF-8 Hex form, which is 6 pairs of hexadecimal digits.
        # Maybe we could do something interesting with emojis at some point
        # IDEA: we can keep track of presence of emojis even if we don't know what it is. Each has a unique string
        # ALSO: PyCharm has functionality to display emojis interestingly

        raw_email_string = raw_email.decode('utf-8')

        # can get all the info you want from this (date sent, whether it's been seen, message ID, subject, addresses
        email_message = email.message_from_string(raw_email_string)

        # this will loop through all the available multiparts in mail
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":  # ignore attachments/html
                body = part.get_payload(decode=True)

                return body.decode('utf-8')

def sendConfirmation(server, mySender):
    # remove "From: " from sender
    mySender = mySender[5::]

    print(sender)

    """This is code to confirm signup for spam emails"""
    server_ssl.sendmail(cap, sender, subject, "thank you")

    print("reply sent to " + sender + ": " + subject + " ; " + "thank you")

def getEmailIDs(myCon, myIncludeSeen):
    # result should be a simple "OK", data[0] is a series of IDs for the emails
    # I don't think data has any element besides [0]
    if myIncludeSeen:
        result, data = myCon.uid('search', None, "ALL") # get all emails in inbox
    else:
        result, data = myCon.search(None, '(UNSEEN)') # get only unread emails in inbox

    return data


con = imaplib.IMAP4_SSL('imap.gmail.com') # get a connection to gmail imap server
cap = "capstonespamtest@gmail.com"
con.login(cap, 'BigMike1') # login
con.select('inbox') # go into inbox

includeSeen = True # this bool is to include read emails in your search. set to true to only get unread
data = getEmailIDs(con, includeSeen) # get ID numbers of emails
ids = data[0].split()  # split IDs

i = len(ids) # i is number of emails found

# Create a secure SSL context for smtp to send email replies
server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server_ssl.ehlo() # optional, called by login()
server_ssl.login(cap, "BigMike1")

for x in reversed(range(i)):  # get newest emails first
    id = ids[x]  # pick unique id corresponding to an email

    # sender = extractSender(con, id)
    # subject = extractSubject(con, id)
    body = extractBody(con, id)

    con.store(id, '-FLAGS', '\\Seen') # mark this email as read (idk if we need lefthand side of expression

    if subject[9:16:] == "confirm":
        sendConfirmation(server_ssl, sender)

server_ssl.close()
