import imaplib
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

    return sender

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

con = imaplib.IMAP4_SSL('imap.gmail.com') #get a connection to gmail imap server
con.login('capstonespamtest@gmail.com', 'BigMike1') #login
con.select('inbox') #go into inbox

# result should be a simple "OK", data[0] is a series of IDs for the emails
# I don't think data has any element besides [0]
result, data = con.uid('search', None, "ALL")

ids = data[0].split() # split IDs

i = len(ids) # i is number of emails found

for x in reversed(range(i)): #get newest emails first
    id = ids[x] # pick unique id corresponding to an email
    sender = extractSender(con, id)
    subject = extractSubject(con, id)
    body = extractBody(con, id)

    print(sender)
    print(subject)
    print(body)

