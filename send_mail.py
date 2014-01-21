import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

from config import GMAIL_USER, GMAIL_PASSWORD

def mail(to, subject, text, attach=None):
   msg = MIMEMultipart()

   msg['From'] = GMAIL_USER
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   if attach:
      part = MIMEBase('application', 'octet-stream')
      part.set_payload(open(attach, 'rb').read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
      msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(GMAIL_USER, GMAIL_PASSWORD)
   mailServer.sendmail(GMAIL_USER, to, msg.as_string())
   mailServer.close()