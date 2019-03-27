import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlLabel
from pyforms.controls import ControlDockWidget

class EmailWindow(BaseWidget):

    def __init__(self):
        self._bodyText = ControlLabel('Body', field_css='max-width:500px;')
        self._panel = ControlDockWidget
        BaseWidget.__init__(self, 'Email body')

if __name__ == "__main__":
    pyforms.start_app(EmailWindow)