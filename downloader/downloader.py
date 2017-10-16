import argparse
import json
import logging
import os
import Queue
import time
import urllib2

logger = logging.getLogger(__name__)


class Error(Exception):
    pass


class UnexpectedImageType(Error):
    pass


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def _parse_input_file(input_file):
    raw = json.load(input_file)
    url_dict = {}
    for key, recipe_data in raw.iteritems():
        url_dict[key] = recipe_data['mainImage']
    return url_dict


def _ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _write_to_file(filepath, content):
    _ensure_directory_exists(os.path.dirname(filepath))
    open(filepath, 'wb').write(content)


def _download_image_data(image_url):
    image_handle = urllib2.urlopen(
        urllib2.Request(
            image_url,
            headers={
                'User-Agent':
                ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '
                 'Safari/537.36')
            }))
    if image_handle.info().type != 'image/jpeg':
        raise UnexpectedImageType('Expected image/jpeg, got ' +
                                  image_handle.info().type)
    return image_handle.read()


def _download_image_urls(url_dict, output_root):
    download_queue = Queue.Queue()

    for key, url in url_dict.iteritems():
        output_filename = key + '.jpg'
        output_path = os.path.join(output_root, output_filename)
        if os.path.exists(output_path):
            continue
        download_queue.put({
            'url': url,
            'destination': output_path,
            'attempts': 0
        })
    logger.info('%d URLs do not exist locally', download_queue.qsize())
    download_delay = 2.0
    while not download_queue.empty():
        logger.info('%d items left in queue', download_queue.qsize())
        item = download_queue.get()
        if item['attempts'] > 5:
            logger.error('Tried to download %s %d times, giving up.',
                         item['url'], item['attempts'])
            continue
        logger.info('Downloading %s', item['url'])

        try:
            _write_to_file(item['destination'],
                           _download_image_data(item['url']))
            download_delay = max(download_delay - 1.0, 2.0)
        except urllib2.HTTPError as e:
            logger.warn('Got error trying to download %s: %s', item['url'], e)
            code_family = (e.code / 100) * 100
            if (code_family == 400) or (code_family == 500):
                item['attempts'] += 1
                download_queue.put(item)
                download_delay = min(30.0, download_delay * 1.75)
            else:
                raise
        time.sleep(download_delay)


def dummy():
    pass


def main(args):
    configure_logging()
    dummy()
    with open(args.input_file) as input_file:
        url_dict = _parse_input_file(input_file)
    logger.info('Read %d input URLs', len(url_dict))
    _download_image_urls(url_dict, args.output_root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='KetoHub Image Downloader',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_root')
    main(parser.parse_args())
