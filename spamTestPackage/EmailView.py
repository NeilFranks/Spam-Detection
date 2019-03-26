from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlLabel
from pyforms.controls import ControlButton


class EmailView(BaseWidget):

    def __init__(self, sender, date, subject, body):
        BaseWidget.__init__(self, 'Email View')

        # Define login screen stuff
        self._senderField = ControlLabel(sender)
        self._dateField = ControlLabel(date)
        self._subjectField = ControlLabel(subject)
        self._bodyField = ControlLabel(body)
        self._prevButton = ControlButton('Previous')
        self._nextButton = ControlButton('Next')

    def update_fields(self, sender, date, subject, body):
        self._senderField.value = sender
        self._dateField.value = date
        self._subjectField.value = subject
        self._bodyField.value = body

if __name__ == '__main__':
    from pyforms import start_app
    start_app(EmailView)