import imaplib
import smtplib
import os
import email
import time

SMTP_PORT = 587
class EDICommunicator():
    def __init__(self, *, username=None, password=None, server=None, output_dir=None, input_dir=None, use_tls=True):
        self.username = username
        self.password = password
        self.server = server
        self.use_tls = use_tls
        if username is not None and password is not None and server is not None:
            self.init_imap()

    def init_imap(self):
        self.imap = imaplib.IMAP4_SSL(self.server)
        self.imap.login(self.username, self.password)
        self.imap.select()

    def set_labels_email(self, email_id: str, labels: str):
        return self.imap.store(email_id, '+FLAGS', '({})'.format(labels))

    def mail_from_str(self, mail_str):
        mail = email.message_from_string(mail_str)
        return mail

    def get_mail_without_label(self, labels:[str]):
        query_str = '(ALL)'
        if labels is not None:
            if type(labels) is str: 
                labels = [labels]
            query_str = 'UNKEYWORD {}'.format(' '.join(labels))
        res, emails = self.imap.search(None, query_str)
        emails = emails[0].split()
        return emails

    def get_mail_with(self, email_id, selection='(BODY.PEEK[])'):
        res, data = self.imap.fetch(email_id, selection)
        return data[0][1] # mail body
        # mail = email.message_from_bytes(data[0][1])
        # return mail

    def send_mail(self, mail, port=SMTP_PORT):
        server = smtplib.SMTP()
        server.connect(self.server, port)
        if self.use_tls:
            server.starttls()
        server.login(self.username, self.password)
        server.sendmail(mail['From'], mail['To'], mail.as_string())
        self.imap.append('INBOX.Sent', '', imaplib.Time2Internaldate(time.time()), mail.as_string())
        server.quit()
