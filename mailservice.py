import smtplib
from email.message import EmailMessage

class SMTP:
    # Module to send email
    def __init__(self, destination_email="", message="TEST", subject="New Mail"):
        self.destination_email = destination_email
        self.subject = subject
        self.message = message
        self.email_user = "uogclothing@gmail.com"
        self.pw = ""  # can't set password like this as not secure. Would need to use RSA keys or similar.

    def send_mail(self):
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(self.email_user, self.pw)

        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.email_user
        msg['To'] = self.destination_email
        msg.set_content(self.message)

        smtp.send_message(msg)
        smtp.quit()
