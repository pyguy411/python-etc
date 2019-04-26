import unittest
from scrape import (get_links_from_page,
                download_file
                    )
from api import get_api_key

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TestAPI(unittest.TestCase):

    def test_get_api_key(self):
        key = get_api_key()
        logger.info("get_api_key: key: %s, length: %s", key, len(key))
        self.assertEqual(len(key), 32)
        self.assertNotEqual(len(key), 50)

class TestScrape(unittest.TestCase):

    def test_get_links(self):
        links = get_links_from_page('paris')
        self.assertTrue(len(links) > 0)

    def test_download(self):
        for link in get_links_from_page('paris'):
            name = download_file(link)
            self.assertIsNot(name, None)
            break  # can't slice a set , so break after one
