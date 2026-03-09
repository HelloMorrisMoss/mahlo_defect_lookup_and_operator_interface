try:
    import commonlog

    lg = commonlog.single_logger()
except ImportError:
    import logging

    lg = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
