import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class FacebookNotifier(object):
    """
    Basic Facebook posting using emails. You can post to a group only if the FB 
    account linked to the used email address has the required permissions.
    """
    def __init__(self, ms_email, ms_password, ms_host='smtp.gmail.com', ms_username=None, ms_port=587):
        """
        Create a new object with given mail server (ms) parameters. If not 
        specified, the email address is used as username (default for GMail).
        """
        if ms_username is None:
            ms_username = ms_email
        self.host, self.port = ms_host, ms_port
        self.email = ms_email
        self.password = ms_password
        self.username = ms_username

    def __send_mail(self, to, subject, text):
        msg = MIMEMultipart()

        msg['From'] = self.email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        mailServer = smtplib.SMTP(self.host, self.port)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.username, self.password)
        mailServer.sendmail(self.email, to, msg.as_string())
        mailServer.close()

    def post_to_group(self, groupid, message):
        to = str(groupid)+"@groups.facebook.com"
        self.__send_mail(to, '', message)

    def post_to_user(self, userid, message):
        to = str(userid)+"@facebook.com"
        self.__send_mail(to, '', message)
