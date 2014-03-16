#!/usr/bin/env python
import sys
from cqlengine import connection
from caliop.config import Configuration

Configuration.load('./tmp/conf.yaml', 'global')
connection.setup(['127.0.0.1:9160'])

from caliop.smtp.agent import DeliveryAgent


if __name__ == '__main__':
    agent = DeliveryAgent()
    data = open(sys.argv[1]).read()
    messages = agent.process(data)
