import imaplib
import email

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

def extractSubject(myCon, myId):
    _, raw_subject = myCon.fetch(myId, '(BODY[HEADER.FIELDS (SUBJECT)])')
    raw_subject_string = raw_subject[0][1].decode('utf-8')
    subject = email.message_from_string(raw_subject_string)

    """
    subject is in the format: "Subject: *Subject*"
    """

    return subject

def extractBody(myCon, myId):
        _, data = myCon.uid('fetch', myId, '(RFC822)')  # get that email

        # get email into byte literal
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')

        # converts byte literal to string removing b''
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

for x in range(i):
    id = ids[x] # pick unique id corresponding to an email
    sender = extractSender(con, id)
    subject = extractSubject(con, id)
    body = extractBody(con, id)

    print(sender)
    print(subject)
    print(body)

