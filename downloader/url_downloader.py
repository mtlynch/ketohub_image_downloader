import urllib2

_USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/61.0.3163.100 Safari/537.36')


class Error(Exception):
    pass


class UnexpectedImageType(Error):
    pass


def download_image_data(image_url):
    image_handle = urllib2.urlopen(
        urllib2.Request(image_url, headers={'User-Agent': _USER_AGENT}))
    if image_handle.info().type != 'image/jpeg':
        raise UnexpectedImageType('Expected image/jpeg, got ' +
                                  image_handle.info().type)
    return image_handle.read()
