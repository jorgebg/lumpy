import unittest
import threading
import smtpd
import smtplib
import asyncore

import lumpy


class MTA(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 8025
        self.recipient = 'example@' + self.host
        self.mxrecords = [ self.host ]
        localaddr, remoteaddr = (self.host, self.port), (self.host, smtplib.SMTP_PORT)
        self.smtp = self.Server(localaddr, remoteaddr)

    def start(self):
        #smtpd.DEBUGSTREAM = sys.stderr
        thread = threading.Thread(target=asyncore.loop)
        thread.daemon = True
        thread.start()

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


class MailSendTest(unittest.TestCase):

    def setUp(self):
        self.host = 'gmail.com'
        self.mail = lumpy.Mail('example@{}'.format(host))

    def test_domain(self):
        self.assertEqual(mail.domain, self.host)

    def test_dnsquery(self):
        self.assertTrue(mail.mxrecords)


class MailSendTest(unittest.TestCase):

    def setUp(self):
        self.mta = MTA()
        self.mta.start()

    def test_send(self):
        mail = lumpy.Mail(self.mta.recipient, mxrecords=self.mta.mxrecords, port=self.mta.port)
        mail.send()

if __name__ == '__main__':
    unittest.main()
