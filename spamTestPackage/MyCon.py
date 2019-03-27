import imaplib
import email
import base64
import quopri
import re


class MyCon:

    def __init__(self):
        self._con = imaplib.IMAP4_SSL('imap.gmail.com')  # get a connection to gmail imap server

    def login(self, my_email, my_password):
        self._email = my_email
        self._password = my_password
        try:
            self._con.login(self._email, self._password)  # login
        except:
            raise ValueError('Incorrect login credentials.\nTry again.')

    """method to get all emails, either unread+read or just unread, from the directory con is in.
    Must select directory first; example: 
    _con.select('inbox') # go into inbox
    """
    def get_email_ids(self, include_seen):
        if include_seen:
            result, data = self._con.uid('search', None, "ALL")  # get all emails in inbox
        else:
            result, data = self._con.uid('search', None, '(UNSEEN)')  # get unreads emails in inbox

        return data[0].split()  # split IDs

    """
    METHODS FOR EXTRACTION OF EMAIL DATA (SENDER, DATE, SUBJECT, AND BODY SO FAR)

    """
    def extract_info(self, my_id):
        _, data = self._con.uid('fetch', my_id, '(RFC822)')  # get that email

        # get email into byte literal
        raw_email = data[0][1]
        # NOTE: At this point, Emojis are in UTF-8 Hex form, which is 6 pairs of hexadecimal digits.
        # Maybe we could do something interesting with emojis at some point
        # IDEA: we can keep track of presence of emojis even if we don't know what it is. Each has a unique string
        # ALSO: PyCharm has functionality to display emojis interestingly

        raw_email_string = raw_email.decode('utf-8')

        # can get all the info you want from this (date sent, whether it's been seen, message ID, subject, addresses
        email_message = email.message_from_string(raw_email_string)

        #initialize stuff so it's easier to debug (see what was missing where)
        sender = "*sender*"
        date = "*date*"
        subject = "*subject*"
        body = "*body*"

        # get body
        # this will loop through all the available multiparts in mail
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":  # ignore attachments/html
                body = part.get_payload(decode=True).decode('utf-8')

        # get sender, date, and subject
        headers = email_message._headers
        for h in headers:
            if h[0] == "From":
                sender = h[1]
            elif h[0] == "Subject":
                subject = h[1]
            elif h[0] == "Date":
                date = h[1]

        return sender, date, subject, body
