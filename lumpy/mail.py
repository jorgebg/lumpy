import errno
import getpass
import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail(object):
    """
    Sends an email to a single recipient straight to his MTA.
    """

    def __init__(self,
                 recipient,
                 sender='{}@example.com'.format(getpass.getuser()),
                 subject='Sir! My sir!',
                 body='A message from their majesty.',
                 content_type='plain',
                 port=smtplib.SMTP_PORT,
                 mxrecords=None):
        self.recipient = recipient
        self.sender = sender
        self.subject = subject
        self.body = body
        self.content_type = content_type
        self.port = port
        self.mxrecords = mxrecords or self.query_mxrecords()

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
        m.attach(MIMEText(self.body, self.content_type))
        return m

    def query_mxrecords(self):
        """
        Looks up for the MX DNS records of the recipient SMTP server
        """
        import dns.resolver
        logging.info('Resolving DNS query...')
        answers = dns.resolver.query(self.domain, 'MX')
        addresses = [answer.exchange.to_text() for answer in answers]
        logging.info(
            '{} records found:\n{}'.format(
                len(addresses), '\n  '.join(addresses)))
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
                server.sendmail(
                    self.sender, [self.recipient], self.message.as_string())
                server.quit()
                return True
        except Exception as e:
            logging.error(e)
            if (isinstance(e, IOError)
                    and e.errno in (errno.ENETUNREACH, errno.ECONNREFUSED)):
                logging.error(
                    'Please check that port {} is open'.format(self.port))
            if logging.root.level < logging.WARN:
                raise e
        return False
