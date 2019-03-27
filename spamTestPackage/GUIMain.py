from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlEmptyWidget
from spamTestPackage.Login import Login
from spamTestPackage.EmailView import EmailView
from spamTestPackage.MyCon import MyCon


class GUIMain(BaseWidget):

    def __init__(self):

        BaseWidget.__init__(self, 'E-Mail Machine')
        self._panel = ControlEmptyWidget()

        """
        load login screen on startup
        """
        self._panel.value = self.make_login_view()

    """
    METHODS TO DEFINE BUTTON ACTIONS"""
    def __login_button_action(self):
        self._email = self._panel._value._emailField.value
        self._pass = self._panel._value._passField.value

        # Get a connection to your email account
        try:
            include_seen = False
            self._myCon = MyCon(self._email, self._pass)
            self._myCon._con.select('inbox')
            self._email_ids = self._myCon.get_email_ids(include_seen)
            self._email_index = 0 # initialize index to first element
        except ValueError as e:
            print(e)

        # Navigate to email screen
        self._panel.value = self.make_email_view()

    def __prev_button_action(self):
        # Decrement email index
        if self._email_index > 0:
            self._email_index -= 1

            # Get args from email at win._index
            sender, date, subject, body = self._myCon.extract_info(self._email_ids[self._email_index])

            # Update fields
            self._panel._value.update_fields(sender, date, subject, body, (self._email_index+1).__str__(), len(self._email_ids).__str__())

    def __next_button_action(self):
        # Decrement email index
        if self._email_index < len(self._email_ids)-1:
            self._email_index += 1

            # Get args from email at win._index
            sender, date, subject, body = self._myCon.extract_info(self._email_ids[self._email_index])

            # Update fields
            self._panel._value.update_fields(sender, date, subject, body, (self._email_index+1).__str__(), len(self._email_ids).__str__())

    """
    METHODS TO CONSTRUCT THE VARIOUS VIEWS
    """
    def make_login_view(self):
        win = Login()
        win.parent = self
        win._emailField.value = 'spiggybensen@gmail.com'
        win._passField.value = 'BigMike1'
        win._button.value = self.__login_button_action
        return win

    def make_email_view(self):

        # Get args from email at self._index
        sender, date, subject, body = self._myCon.extract_info(self._email_ids[self._email_index])

        # Make window
        win = EmailView(sender, date, subject, body, (self._email_index+1).__str__(), len(self._email_ids).__str__())
        win.parent = self

        # Define button action
        win._prevButton.value = self.__prev_button_action
        win._nextButton.value = self.__next_button_action

        return win

if __name__ == '__main__':
    from pyforms import start_app
    start_app(GUIMain)
