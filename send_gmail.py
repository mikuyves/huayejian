import os
from gmail import GMail, Message


GMAIL_ACCOUNT = os.environ.get('GMAIL_ACCOUNT')
GMAIL_PASSWD = os.environ.get('GMAIL_PASSWD')
MAIL_TO = os.environ.get('MAIL_TO')


class Email():
    def __init__(self, title, text, attachments=None):
        self.title = title
        self.text = text
        self.attachments = attachments

    def send(self):
        print('Sending {}'.format(self.title))
        gmail = GMail(GMAIL_ACCOUNT, GMAIL_PASSWD)
        msg = Message(self.title,
                      to=MAIL_TO,
                      text=self.text,
                      attachments=self.attachments
                      )
        gmail.send(msg)
        gmail.close()
        print('Ok. Sent Edison: {}'.format(self.title))
