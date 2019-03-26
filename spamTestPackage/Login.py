from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlPassword


class Login(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'Login')

        # Define login screen stuff
        self._emailField = ControlText('Email')
        self._passField = ControlPassword('Password')
        self._button = ControlButton('Login')

if __name__ == '__main__':
    from pyforms import start_app
    start_app(Login)