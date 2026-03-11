try:
    import commonlog

    lg = commonlog.single_logger()
    # pip install upgrade C:/Users/lmcglaughlin/PycharmProjects/commonlog
except ImportError:
    import logging

    lg = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
