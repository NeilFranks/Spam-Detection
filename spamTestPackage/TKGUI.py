from tkinter import *
import os
from spamTestPackage.MyCon import MyCon
from spamTestPackage.Email import Email
from spamTestPackage.CommonCounter import CommonCounter

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

        # define stuff on page
        self.subframe = Frame(self)
        self.count = Button(self.subframe, text="Count common words and phrases", command=self.count_common)
        self.spam_check = Button(self.subframe, text="Is this spam?", command=self.check_for_spam)

        self.display_list = Listbox(self, width=50)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.email_body = Text(self)
        self.body_scrollbar = Scrollbar(self.email_body, orient=VERTICAL)

    def show_list(self):

        # pack in
        self.count.pack(side=LEFT)
        self.spam_check.pack(side=RIGHT)
        self.subframe.pack(side=TOP, fill=X)

        # retrieve ID numbers of all emails
        include_seen = True
        _myCon._con.select('inbox')
        self._email_ids = _myCon.get_email_ids(include_seen)
        print("number of emails retrieved: "+len(self._email_ids).__str__())

        # Use id numbers to get every email into a list
        self._list_of_emails = []
        for id in self._email_ids:
            sender, date, subject, body = _myCon.extract_info(id)
            mail = Email(sender, date, subject, body)
            self._list_of_emails.insert(0, mail) # insert at front so newest emails are at front

        self.display_list.pack(side=LEFT, fill=BOTH)

        # populate list
        for email in self._list_of_emails:
            self.display_list.insert(END, email.get_sender())

        # bind scrollbar to list of emails
        self.scrollbar.pack(side=LEFT, fill=Y)
        self.scrollbar.config(command=self.display_list.yview)
        self.display_list.config(yscrollcommand=self.scrollbar.set)
        self.display_list.bind('<<ListboxSelect>>', self.get_select)

        # bind another scrollbar to the body text
        self.body_scrollbar.pack(side=RIGHT, fill=Y)
        self.body_scrollbar.config(command=self.email_body.yview)
        self.email_body['yscrollcommand'] = self.body_scrollbar.set

        # show email body text
        self.email_body.config(wrap=CHAR, state=DISABLED)
        self.email_body.pack(side=RIGHT, fill=BOTH, expand=True)

    def get_select(self, event):
        # remember selected email
        display_list = event.widget
        index = int(display_list.curselection()[0])
        self.selected_email = self._list_of_emails[index]

        self.email_body.config(state=NORMAL)
        self.email_body.delete('1.0', END)
        self.email_body.insert(END, "Subject: " + self.selected_email.get_subject() + "\n\n"
                               + self.selected_email.get_body())
        self.email_body.config(state=DISABLED)

    def count_common(self):
        subWords, sub2, sub3, sub4, sub5 = _subject_counter.get_common(self._list_of_emails, 500)
        bodyWords, body2, body3, body4, body5 = _body_counter.get_common(self._list_of_emails, 500)

        message = "SUBJECT\nSingle words: "+subWords.__str__()+"\n\n2 words: "+sub2.__str__()+"\n\n3 words: "\
                  +sub3.__str__()+"\n\n4 words: "+sub4.__str__()+"\n\n5 words: "+sub5.__str__()+"\n\nBODY\n\nSingle words: "\
                  +bodyWords.__str__()+"\n\n2 words: "+body2.__str__()+"\n\n3 words: "+body3.__str__()+"\n\n4 words: "\
                  +body4.__str__()+"\n\n5 words: "+body5.__str__()+"\n"


        self.email_body.config(state=NORMAL)
        self.email_body.delete('1.0', END)
        self.email_body.insert(END, message)
        self.email_body.config(state=DISABLED)

    def check_for_spam(self):
        return 0

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
    _subject_counter = CommonCounter("subject")
    _body_counter = CommonCounter("body")

    root = Tk()

    # declare the various pages
    p1 = Login(root)
    p2 = EmailList(root)

    # initialize main viewer which places all pages into the window
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1200x600")
    root.wm_title("E-Mail Machine")

    #add icon
    base_folder = os.path.dirname(__file__)
    image_path = os.path.join(base_folder, 'icon.bmp')
    root.wm_iconbitmap(image_path) #not working for some reason, just makes icon blank

    root.mainloop()