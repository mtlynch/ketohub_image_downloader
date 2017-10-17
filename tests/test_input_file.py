import io
import unittest

from downloader import input_file


class InputFileTest(unittest.TestCase):

    def test_parse_empty_input_file_yields_empty_dict(self):
        mock_file = io.BytesIO('{}')

        self.assertEqual(input_file.parse(mock_file), {})

    def test_parse_valid_input_file_yields_valid_url_dictionary(self):
        mock_file = io.BytesIO("""
        {
          "key1": {
            "blah": "foo",
            "mainImage": "https://mock.com/foo/main-image.jpg"
          },
          "key2": {
            "blah": "foo",
            "mainImage": "https://mock.com/bar/main-image.jpg"
          }
        }
        """)

        self.assertEqual(
            input_file.parse(mock_file), {
                'key1': 'https://mock.com/foo/main-image.jpg',
                'key2': 'https://mock.com/bar/main-image.jpg'
            })
