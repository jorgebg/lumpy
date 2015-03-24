import sys
import argparse
import getpass
import errno
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail(object):
    """
    Sends an email to a single recipient straight to his MTA.
    """

    def __init__(self, recipient, sender=None, subject=None, body=None, port=None, mxrecords=None,  verbose = False):
        self.verbose = verbose

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
        if self.verbose:
            print('Resolving DNS query...')
        answers = dns.resolver.query(self.domain, 'MX')
        addresses = [answer.exchange.to_text() for answer in answers]
        if self.verbose:
            print('{} records found:'.format(len(addresses)))
            for a in addresses:
                print('  {}'.format(a))
            print('')
        return addresses

    def send(self):
        """
        Attempts the delivery through recipient's domain MX records.
        """
        try:
            for mx in self.mxrecords:
                if self.verbose:
                    print('Connecting to {} {}...'.format(mx, self.port))
                server = smtplib.SMTP(mx, self.port)
                server.set_debuglevel(self.verbose)
                server.sendmail(self.sender, [self.recipient], self.message.as_string())
                server.quit()
                break
        except IOError as e:
            if e.errno in (errno.ENETUNREACH, errno.ECONNREFUSED):
                sys.stderr.writelines('Looks like port {} is blocked: {}\n'.format(self.port, e))
            if self.verbose:
                raise e

    class Defaults:
        Sender = '{}@example.com'.format(getpass.getuser())
        Subject = 'Sir! My sir!'
        Body = 'A message from their majesty.'
        Port = smtplib.SMTP_PORT


class App(object):

    def run(self):
        args = self.parse()
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
