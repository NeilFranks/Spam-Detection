
import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList
from spamTestPackage.Two_Window_GUI.Email import Email
from spamTestPackage.Two_Window_GUI.EmailWindow import EmailWindow
from spamTestPackage.MyCon import MyCon
from pyforms import settings as formSettings
formSettings.PYFORMS_STYLESHEET = 'style.css'

class EmailList(BaseWidget):

    def __init__(self):
        BaseWidget.__init__(self, 'Email List')
        self._list_of_emails = list()
        self._emailList = ControlList('Emails', item_selection_changed_event=self.__get_body)
        self._emailList.horizontal_headers = ['Sender', 'Date', 'Subject']
        self._emailList.readonly = True
        self._emailList.select_entire_row = True
        self._email = 'capstonespamtest@gmail.com'
        self._pass = 'BigMike1'
        self._panel = EmailWindow()
        self._panel.parent = self

        # Get a connection to your email account
        try:
            include_seen = True
            self._myCon = MyCon(self._email, self._pass)
            self._myCon._con.select('inbox')
            self._email_ids = self._myCon.get_email_ids(include_seen)
            self._email_index = 0  # initialize index to first element
        except ValueError as e:
            print(e)

        index = 0
        for email in self._email_ids:
            sender, date, subject, body = self._myCon.extract_info(email)
            mail = Email(index, sender, date, subject, body)
            self._list_of_emails.append(mail)
            self._emailList.__add__([mail.get_sender(), mail.get_date(), mail.get_subject()])
        self._emailList.resize_rows_contents()

    def __get_body(self):
        index = self._emailList.selected_row_index
        if index is not None:
            self._panel._bodyText.value = self._list_of_emails[index].get_body()
            self._panel.show()



if __name__ == "__main__":
    pyforms.start_app(EmailList)

