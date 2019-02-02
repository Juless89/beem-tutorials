from datetime import datetime
import smtplib


class Gmail():
    def __init__(self, cooldown):
        self.gmail_user = ''
        self.to = ''
        self.gmail_password = ''
        self.last_mail_sent = None
        self.cooldown = cooldown

    # Verify that the last email sent is longer than cooldown seconds ago.
    # Sort for different types of operations.
    def check_cooldown(self, type):
        if type == 'transfer':
            if not self.last_mail_sent:
                self.last_mail_sent = datetime.now()
                return True
            elif ((datetime.now()-self.last_mail_sent).total_seconds()
                    > self.cooldown):
                self.last_mail_sent = datetime.now()
                return True
            else:
                return False
        elif type == 'vote':
            return True

    # Compose and send email via secure login.
    def send_email(self, subject, text, type):
        BODY = (
                "From: %s" % self.gmail_user,
                "To: %s" % self.to,
                "Subject: %s" % subject,
                "",
                text
                )
        MAIL = "\r\n".join(BODY)

        if self.check_cooldown(type):
            try:
                server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server_ssl.ehlo()
                server_ssl.login(self.gmail_user, self.gmail_password)
                server_ssl.sendmail(self.gmail_user, self.to, MAIL)
            except Exception as e:
                print('Something went wrong...', e)
            finally:
                server_ssl.close()
