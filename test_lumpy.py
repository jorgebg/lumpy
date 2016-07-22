import asyncore
import errno
import logging
import smtpd
import smtplib
import socket
import sys
import threading
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import lumpy


class MTAMock(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 8025
        self.recipient = 'example@' + self.host
        self.mxrecords = [self.host]
        localaddr = (self.host, self.port)
        remoteaddr = (self.host, smtplib.SMTP_PORT)
        self.smtp = self.Server(localaddr, remoteaddr)

    def start(self):
        thread = threading.Thread(target=asyncore.loop)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.smtpd.close()

    class Server(smtpd.SMTPServer):
        def process_message(self, peer, mailfrom, rcpttos, data):
            log = smtpd.DEBUGSTREAM
            inheaders = 1
            lines = data.split('\n')
            log.write('---------- MESSAGE FOLLOWS ----------')
            for line in lines:
                if inheaders and not line:
                    log.write('X-Peer: {}'.format(peer[0]))
                    inheaders = 0
                log.write(line)
            log.write('------------ END MESSAGE ------------')

MTA = MTAMock()
MTA.start()


class MailTest(unittest.TestCase):

    def setUp(self):
        self.host = 'gmail.com'
        self.mail = lumpy.Mail('example@{}'.format(self.host))

    def test___init__(self):
        with self.assertRaises(ValueError):
            lumpy.Mail('p3nwed')
        lumpy.Mail('bmo@ooo.land', mxrecords='smtp1.ooo.land,smtp2.ooo.land')

    def test_domain(self):
        self.assertEqual(self.mail.domain, self.host)

    def test_dnsquery(self):
        self.assertTrue(self.mail.mxrecords)

    def test_message(self):
        mail = self.mail
        msg = mail.message
        self.assertTrue(isinstance(msg, MIMEMultipart))

        self.assertEqual(msg['Subject'], mail.subject)
        self.assertEqual(msg['From'], mail.sender)
        self.assertEqual(msg['To'], mail.recipient)
        self.assertTrue(len(msg.get_payload()))
        body = msg.get_payload(0)
        self.assertTrue(isinstance(body, MIMEText))
        self.assertEqual(body.get_payload(), mail.body)


class MailSendTest(unittest.TestCase):

    def test_send(self):
        mail = lumpy.Mail(
            MTA.recipient, mxrecords=MTA.mxrecords, port=MTA.port)
        self.assertTrue(mail.send())

        for no in (errno.ENETUNREACH, errno.ECONNREFUSED):

            def sendmailmock(self, *args, **kwargs):
                raise socket.error(no, errno.errorcode[no])
            sendmail = smtplib.SMTP.sendmail
            smtplib.SMTP.sendmail = sendmailmock

            logging.root.level = logging.INFO
            with self.assertRaises(IOError):
                mail.send()
            logging.root.level = logging.WARN
            self.assertFalse(mail.send())

            smtplib.SMTP.sendmail = sendmail


class MainTest(unittest.TestCase):

    def setUp(self):
        self.oldargv = sys.argv

        args = {
            'recipient': MTA.recipient,
            'mxrecords': ','.join(MTA.mxrecords),
            'port': MTA.port
        }

        self.argv = ('lumpy {recipient} --mxrecords {mxrecords} --port {port}'
                     .format(**args).split(' '))

    def tearDown(self):
        sys.argv = self.oldargv

    def test_run(self):
        sys.argv = self.argv
        lumpy.run()

    def test_run_verbose(self):
        sys.argv = self.argv + ['--verbose']
        lumpy.run()


if __name__ == '__main__':
    unittest.main()
