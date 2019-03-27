

class Email:

    def __init__(self, index, sender, date, subject, body):
        self._index = index
        self._sender = sender
        self._date = date
        self._subject = subject
        self._body = body

    def get_index(self):
        return self._index

    def get_sender(self):
        return self._sender

    def get_date(self):
        return self._date

    def get_subject(self):
        return self._subject

    def get_body(self):
        return self._body