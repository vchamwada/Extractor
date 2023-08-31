import unittest
import os
import queue
from io import StringIO
from unittest.mock import patch
from extractor import fetch_url, process_markup, producer_consumer


class TestWebLinkExtractor(unittest.TestCase):
    def test_fetch_url(self):
        # Mock the requests.get function to return a response
        with patch("requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.text = '<a href="link1">Link 1</a><a href="link2">Link 2</a>'

            markup_queue = queue.Queue()
            fetch_url("http://example.com", markup_queue)

            # Check if the fetched markup is added to the queue
            self.assertEqual(markup_queue.qsize(), 1)
            self.assertEqual(markup_queue.get(), mock_response.text)

    def test_process_markup(self):
        # Create a mock output file
        output_file = StringIO()

        # Mock BeautifulSoup and process_markup
        with patch("extractor.BeautifulSoup") as mock_bs:
            mock_soup_instance = mock_bs.return_value
            mock_soup_instance.find_all.return_value = [
                {"href": "link1"},
                {"href": "link2"},
            ]

            markup = '<html><a href="link1">Link 1</a><a href="link2">Link 2</a></html>'
            process_markup(markup, output_file)

            # Get the content from the output_file
            output_file.seek(0)
            content = output_file.read()

            # Check if the parsed links are in the content
            expected_output = "link1\nlink2\n"
            self.assertEqual(content, expected_output)

    def test_producer_consumer(self):
        # Mock the fetch_url function to add markup to the queue
        def mock_fetch_url(url, markup_queue):
            markup_queue.put('<a href="link1">Link 1</a><a href="link2">Link 2</a>')

        url_list = ["http://example.com"]
        output_file = "test_output.txt"
        max_queue_size = 10

        with patch("extractor.fetch_url", side_effect=mock_fetch_url):
            producer_consumer(url_list, output_file, max_queue_size)

            # Check if the output file was created and contains the parsed links
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, "r") as file:
                content = file.read()
                expected_output = "link1\nlink2\n"
                self.assertEqual(content, expected_output)

            # Clean up the test output file
            os.remove(output_file)


if __name__ == "__main__":
    unittest.main()
