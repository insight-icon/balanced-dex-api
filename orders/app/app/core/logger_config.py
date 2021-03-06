import sys

from loguru import logger
import logging
import logstash


class LoggerConfig:
    # TODO: refactor this
    def __init__(self):
        # Note: use "backtrace" and "diagnose" in production,
        # Note: backtrace and diagnose will LEAK sensitive data
        logger.add("backend.log",
                   enqueue=True,
                   rotation="5 MB"
                   # backtrace=True,
                   # diagnose=True
                   )

        # handler = logging.handlers.SysLogHandler(address=('localhost', 5000))
        # logger.add(handler)
        logger.add(logstash.LogstashHandler("localhost", 5000, version=1))
        # for udp - logstash.LogstashHandler("localhost", 5000, version=1)
        # for tcp - logstash.TCPLogstashHandler(host, 5959, version=1)

        # add extra field to logstash message
        extra = {
            'test_string': 'python version: ' + repr(sys.version_info),
            'test_boolean': True,
            'test_dict': {'a': 1, 'b': 'c'},
            'test_float': 1.23,
            'test_integer': 123,
            'test_list': [1, 2, '3'],
        }
        logger.info('python-logstash: test extra fields{extra}', extra=extra)

