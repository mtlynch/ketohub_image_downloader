import argparse
import logging
import os
import Queue
import time
import urllib2

import input_file
import jobs
import url_downloader

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


def _ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _write_to_file(filepath, content):
    _ensure_directory_exists(os.path.dirname(filepath))
    open(filepath, 'wb').write(content)


def _process_download_jobs(job_list):
    download_queue = Queue.Queue()
    for job in job_list:
        if not os.path.exists(job.output_path()):
            download_queue.put(job)

    logger.info('%d URLs do not exist locally', download_queue.qsize())
    download_delay = 2.0
    while not download_queue.empty():
        logger.info('%d jobs left in queue', download_queue.qsize())
        job = download_queue.get()
        if job.attempts() > 5:
            logger.error('Tried to download %s %d times, giving up.',
                         job.url(), job.attempts())
            continue
        logger.info('Downloading %s', job.url())

        try:
            _write_to_file(job.output_path(),
                           url_downloader.download_image_data(job.url()))
            download_delay = max(download_delay - 1.0, 2.0)
        except urllib2.HTTPError as e:
            logger.warn('Got error trying to download %s: %s', job.url(), e)
            code_family = (e.code / 100) * 100
            if (code_family == 400) or (code_family == 500):
                job.record_attempt()
                download_queue.put(job)
                download_delay = min(30.0, download_delay * 1.75)
            else:
                raise
        except url_downloader.UnexpectedImageType as e:
            logger.warn('Unexpected image trying to download %s: %s',
                        job.url(), e)
        time.sleep(download_delay)


def main(args):
    configure_logging()
    logger.info('--input_file=%s', args.input_file)
    logger.info('--output_root=%s', args.output_root)
    with open(args.input_file) as input_file_handle:
        url_dict = input_file.parse(input_file_handle)
    logger.info('Read %d input URLs', len(url_dict))
    job_list = jobs.from_url_dict(url_dict, args.output_root)
    _process_download_jobs(job_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='KetoHub Image Downloader',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_root')
    main(parser.parse_args())
