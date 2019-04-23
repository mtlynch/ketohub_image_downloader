import unittest
import urllib2

import mock

from downloader import url_downloader


class UrlDownloaderTest(unittest.TestCase):

    def setUp(self):
        mock_urlopen_patch = mock.patch(
            'downloader.url_downloader.urllib2.urlopen', autospec=True)
        self.addCleanup(mock_urlopen_patch.stop)
        self.mock_urlopen = mock_urlopen_patch.start()

        mock_request_patch = mock.patch(
            'downloader.url_downloader.urllib2.Request', autospec=True)
        self.addCleanup(mock_request_patch.stop)
        self.mock_request = mock_request_patch.start()

    def test_download_succeeds_when_server_is_ok(self):
        mock_handle = mock.Mock()
        mock_handle.info.return_value = mock.Mock(type='image/jpeg')
        mock_handle.read.return_value = 'dummy image data'
        self.mock_urlopen.return_value = mock_handle
        self.assertEqual(
            url_downloader.download_image_data('http://mock.com/image.jpg'),
            'dummy image data')
        self.assertEqual('http://mock.com/image.jpg',
                         self.mock_request.call_args[0][0])

    def test_encodes_special_characters(self):
        mock_handle = mock.Mock()
        mock_handle.info.return_value = mock.Mock(type='image/jpeg')
        mock_handle.read.return_value = 'dummy image data'
        self.mock_urlopen.return_value = mock_handle
        self.assertEqual(
            url_downloader.download_image_data(
                u'https://lowcarbyum.com/wp-content/uploads/2017/12/atkins-cafe\u0301-caramel-shake-breakfast-muffins-fb.jpg'
            ), 'dummy image data')
        self.assertEqual(
            'https://lowcarbyum.com/wp-content/uploads/2017/12/atkins-cafe%CC%81-caramel-shake-breakfast-muffins-fb.jpg',
            self.mock_request.call_args[0][0])

    def test_download_fails_when_server_returns_403(self):
        self.mock_urlopen.side_effect = urllib2.HTTPError(url='',
                                                          code=404,
                                                          msg='',
                                                          hdrs=None,
                                                          fp=None)
        with self.assertRaises(urllib2.HTTPError):
            url_downloader.download_image_data('http://mock.com/image.jpg')

    def test_download_fails_when_content_type_is_not_jpeg(self):
        mock_handle = mock.Mock()
        mock_handle.info.return_value = mock.Mock(type='image/faketype')
        mock_handle.read.return_value = 'dummy image data'
        self.mock_urlopen.return_value = mock_handle
        with self.assertRaises(url_downloader.UnexpectedImageType):
            url_downloader.download_image_data('http://mock.com/image.jpg')
