from gsmtpd import SMTPServer
from cqlengine import connection
from caliop.config import Configuration

Configuration.load('./tmp/conf.yaml', 'global')
connection.setup(['127.0.0.1:9160'])

from caliop.helpers.log import log
from caliop.mda.agent import DeliveryAgent


class SmtpServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        agent = DeliveryAgent()
        messages = agent.process(data)
        log.info('Deliver of %d messages' % len(messages))


if __name__ == '__main__':
    s = SmtpServer(("127.1", 4000))
    s.serve_forever()
