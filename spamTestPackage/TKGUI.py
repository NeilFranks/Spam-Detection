from tkinter import *
from spamTestPackage.MyCon import MyCon
from spamTestPackage.Email import Email

class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Login(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # define stuff
        self.emailLabel = Label(self, text="Email: ")
        self.passwordLabel = Label(self, text="Password: ")
        self.email = Entry(self, width=30)
        self.password = Entry(self, show="*", width=30)
        self.login = Button(self, text="Login", command=self.login_action)
        self.errorMessage = Label(self)

        """
        TO-DO: Implement "remember me" functionality
        """
        # for convenience's sake, I'm filling in email and password.
        self.email.insert(0,"spiggybensen@gmail.com")
        self.password.insert(0,"BigMike1")

        # pack stuff in grid layout
        self.emailLabel.grid(row=0, column=0, sticky=E)
        self.passwordLabel.grid(row=1, column=0, sticky=E)
        self.email.grid(row=0, column=1, sticky=W)
        self.password.grid(row=1, column=1, sticky=W)
        self.login.grid(columnspan=2, row=2, column=0)

    def login_action(self):
        try:
            _myCon.login(self.email.get(), self.password.get())
            p2.show_list()
            p2.lift()
        except ValueError as e:
            self.errorMessage.config(text=e)
            self.errorMessage.grid(columnspan=2, row=3, column=0)

class EmailList(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def show_list(self):

        # retrieve ID numbers of all emails
        include_seen = True
        _myCon._con.select('inbox')
        self._email_ids = _myCon.get_email_ids(include_seen)

        # Use id numbers to get every email into a list
        self._list_of_emails = []
        for id in self._email_ids:
            sender, date, subject, body = _myCon.extract_info(id)
            mail = Email(sender, date, subject, body)
            self._list_of_emails.append(mail)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        display_list = Listbox(self, yscrollcommand=scrollbar.set)
        for email in self._list_of_emails:
            display_list.insert(END, email.get_subject()+"\n"+email.get_sender())

        display_list.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command = display_list.yview)

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p1.show()

if __name__ == "__main__":
    _myCon = MyCon()
    root = Tk()

    # declare the various pages
    p1 = Login(root)
    p2 = EmailList(root)

    # initialize main viewer which places all pages into the window
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()