import argparse
import logging

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def dummy():
    pass


def main(args):
    configure_logging()
    dummy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='KetoHub Image Downloader',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_file')
    main(parser.parse_args())
