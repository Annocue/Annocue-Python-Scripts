import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email():
  def __init__(self, user, pwd, recipient, subject, html, text=''):
    self.user = user
    self.pwd = pwd
    self.recipient = recipient
    self.subject = subject
    self.html = html
    self.text = text
  def send(self):
    gmail_user = self.user
    gmail_pwd = self.pwd
    FROM = self.user
    TO = self.recipient if type(self.recipient) is list else [self.recipient]
    SUBJECT = self.subject
    HTML = self.html
    TEXT = self.text

    # Prepare actual message
    message = MIMEMultipart('alternative')
    message['Subject'] = SUBJECT
    message['From'] = FROM
    message['To'] = ', '.join(TO)

    # The last message attached is the preferred format
    message.attach(MIMEText(TEXT, 'plain'))
    message.attach(MIMEText(HTML, 'html'))

    try:
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.ehlo()
      server.starttls()
      server.login(gmail_user, gmail_pwd)
      server.sendmail(FROM, TO, message.as_string())
      server.close()
      print('successfully sent email to ' + ','.join(TO))
    except:
      print('failed to send mail to ' + ','.join(TO))
