from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlLabel
from pyforms.controls import ControlButton


class EmailView(BaseWidget):

    def __init__(self, sender, date, subject, body, id, total):
        BaseWidget.__init__(self, 'Email View')

        # Define email view
        self._senderLabel = ControlLabel("Sent from:")
        self._senderField = ControlLabel(sender)
        self._dateLabel = ControlLabel("Date sent:")
        self._dateField = ControlLabel(date)
        self._subjectLabel = ControlLabel("Subject:")
        self._subjectField = ControlLabel(subject)
        self._bodyField = ControlLabel(body)

        # Define indexing stuff
        self._indexLabel = ControlLabel(id + " of " + total)
        self._prevButton = ControlButton('Previous')
        self._nextButton = ControlButton('Next')

    def update_fields(self, sender, date, subject, body, id, total):
        self._senderField.value = sender
        self._dateField.value = date
        self._subjectField.value = subject
        self._bodyField.value = body
        self._indexLabel.value = (id + " of " + total)

if __name__ == '__main__':
    from pyforms import start_app
    start_app(EmailView)