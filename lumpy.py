import logging
import argparse
import getpass
import errno
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dns.resolver

class Mail(object):

    def __init__(self, recipient=None, sender=None, subject=None, body=None):
        self.recipient = recipient
        self.sender = sender or '{}@example.com'.format(getpass.getuser())
        self.subject = subject or 'Sir! My sir!'
        self.body = body or 'A message from their majesty.'
        self.verbose = False

    @property
    def domain(self):
        m = re.match(r'.+@(\w+\.\w+)', self.recipient)
        if m:
            return m.group(1)
        else:
            raise ValueError('Unable to get recipient domain')

    @property
    def message(self):
        m = MIMEMultipart('alternative')
        m['Subject'] = self.subject
        m['From'] = self.sender
        m['To'] = self.recipient
        m.attach(MIMEText(self.body, 'plain'))
        return m

    def send(self):
        """
        Sends an email to a single recipient straight to his MTA.
        Looks up for the MX DNS records of the recipient SMTP server and attempts the delivery through them.
        """
        answers = dns.resolver.query(self.domain, 'MX')
        try:
            for answer in answers:
                ex = answer.exchange.to_text()
                server = smtplib.SMTP(ex)
                server.set_debuglevel(self.verbose)
                server.sendmail(self.sender, [self.recipient], self.message.as_string())
                server.quit()
        except OSError as e:
            if e.errno is errno.ENETUNREACH:
                print('Looks like port 25 is blocked')
            raise e


class App(object):

    def run(self):
        mail = Mail()
        self.parse(mail)
        mail.send()

    @classmethod
    def parse(cls, mail):
        parser = argparse.ArgumentParser(prog='lumpy', description=mail.send.__doc__)
        arg = parser.add_argument

        arg('--from', '-f', nargs='?', dest='sender')
        arg('recipient')
        arg('--subject', '-s', nargs='?')
        arg('--body', '-b', nargs='?')
        arg('--verbose', '-v', action='store_true')
        
        parser.parse_args(namespace=mail)


if __name__ == "__main__":
    App().run()
