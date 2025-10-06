# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------

import unittest
from unittest.mock import Mock, patch
import io

from skbio.io._iosources import HTTPSource


class TestHTTPSourceMock(unittest.TestCase):
    """Unit tests for HTTPSource using mocking."""

    def setUp(self):
        self.url = 'http://example.com/data.txt'
        self.options = {}

    def test_can_read_http_url(self):
        # Test that HTTPSource can identify HTTP URLs
        source = HTTPSource(self.url, self.options)
        self.assertTrue(source.can_read())

    def test_can_read_https_url(self):
        # Test that HTTPSource can identify HTTPS URLs
        https_url = 'https://example.com/data.txt'
        source = HTTPSource(https_url, self.options)
        self.assertTrue(source.can_read())

    def test_can_read_non_http_url(self):
        # Test that HTTPSource rejects non-HTTP URLs
        ftp_url = 'ftp://example.com/data.txt'
        source = HTTPSource(ftp_url, self.options)
        self.assertFalse(source.can_read())

    @patch('skbio.io._iosources.requests.get')
    def test_get_reader_successful(self, mock_get):
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.content = b'test data content'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        source = HTTPSource(self.url, self.options)
        reader = source.get_reader()

        # Verify requests.get was called with the URL
        mock_get.assert_called_once_with(self.url)

        # Verify raise_for_status was called
        mock_response.raise_for_status.assert_called_once()

        # Verify reader returns correct content
        self.assertIsInstance(reader, io.BufferedReader)
        content = reader.read()
        self.assertEqual(content, b'test data content')

    @patch('skbio.io._iosources.requests.get')
    def test_get_reader_http_error(self, mock_get):
        # Mock HTTP error response (404, 500, etc.)
        import requests
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        source = HTTPSource(self.url, self.options)

        # Verify that HTTPError is raised
        with self.assertRaises(requests.HTTPError):
            source.get_reader()

        # Verify requests.get was called
        mock_get.assert_called_once_with(self.url)


if __name__ == "__main__":
    unittest.main()
