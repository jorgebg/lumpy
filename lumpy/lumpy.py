import sys
import argparse
import getpass
import errno
import re
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail(object):
    """
    Sends an email to a single recipient straight to his MTA.
    """

    def __init__(self, recipient, sender=None, subject=None, body=None, port=None, mxrecords=None):
        self.recipient = recipient
        self.sender = sender or self.Defaults.Sender
        self.subject = subject or self.Defaults.Subject
        self.body = body or self.Defaults.Body
        self.port = port or self.Defaults.Port

        if not mxrecords:
            mxrecords = self.dnsquery()
        elif isinstance(mxrecords, str):
            mxrecords = mxrecords.split(',')
        self.mxrecords = mxrecords

    @property
    def domain(self):
        m = re.match(r'.+@(.+)', self.recipient)
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

    def dnsquery(self):
        """
        Looks up for the MX DNS records of the recipient SMTP server
        """
        import dns.resolver
        logging.info('Resolving DNS query...')
        answers = dns.resolver.query(self.domain, 'MX')
        addresses = [answer.exchange.to_text() for answer in answers]
        logging.info('{} records found:\n{}'.format(len(addresses), '\n  '.join(addresses)))
        return addresses

    def send(self):
        """
        Attempts the delivery through recipient's domain MX records.
        """
        try:
            for mx in self.mxrecords:
                logging.info('Connecting to {} {}...'.format(mx, self.port))
                server = smtplib.SMTP(mx, self.port)
                server.set_debuglevel(logging.root.level < logging.WARN)
                server.sendmail(self.sender, [self.recipient], self.message.as_string())
                server.quit()
                return True
        except Exception as e:
            logging.error(e)
            if isinstance(e, IOError) and e.errno in (errno.ENETUNREACH, errno.ECONNREFUSED):
                logging.error('Please check that port {} is open'.format(self.port))
            if logging.root.level < logging.WARN:
                raise e
        return False

    class Defaults:
        Sender = '{}@example.com'.format(getpass.getuser())
        Subject = 'Sir! My sir!'
        Body = 'A message from their majesty.'
        Port = smtplib.SMTP_PORT


class App(object):

    def run(self):
        args = self.parse()
        if args.verbose:
            logging.root.level = logging.INFO
        del args.verbose
        Mail(**args.__dict__).send()

    @classmethod
    def parse(cls):
        parser = argparse.ArgumentParser(prog='lumpy', description=Mail.send.__doc__)
        arg = parser.add_argument

        arg('--from', '-f', nargs='?', dest='sender')
        arg('recipient', metavar='recipient@example.com')
        arg('--subject', '-s', nargs='?')
        arg('--body', '-b', nargs='?')
        arg('--port', '-p', nargs='?')
        arg('--mxrecords', '--mx', '-m', nargs='?', help="List of comma-separated mx records")
        arg('--verbose', '-v', action='store_true')

        return parser.parse_args()
