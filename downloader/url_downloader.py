import urllib2
import urlparse

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/61.0.3163.100 Safari/537.36')


class Error(Exception):
    pass


class UnexpectedImageType(Error):
    pass


def download_image_data(image_url):
    image_handle = urllib2.urlopen(
        urllib2.Request(_encode_url(image_url),
                        headers={'User-Agent': _USER_AGENT}))
    if image_handle.info().type not in ['image/jpeg', 'image/png']:
        raise UnexpectedImageType('Unexpected image type: ' +
                                  image_handle.info().type)
    return image_handle.read()


def _encode_url(url):
    scheme, network_location, path, query, fragment_identifier = urlparse.urlsplit(
        url)
    path = urllib2.quote(path.encode('utf8'))
    return urlparse.urlunsplit(
        (scheme, network_location, path, query, fragment_identifier))
