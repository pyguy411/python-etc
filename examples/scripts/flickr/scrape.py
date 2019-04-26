import logging
import os.path
import re
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from multiprocessing import Lock
from urllib.parse import quote
from urllib.request import (
    urlopen,
)

from sqlite_functions import (
    create_table_in_DB,
    insert_into_DB
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
lock = Lock()

SUPPORTED_IMAGE_TYPES = ('.jpg', '.png', '.gif')


def get_links_from_page(text: str=None) -> set:
    """
    extract the links from the HTML

    :param text: the search term
    :return: a set of links
    :rtype: set
    """
    links = set()
    link_pattern = re.compile('img.src=.+')  # todo expand this to get href's
    # link_pattern = re.compile(r'href=*')
    if text:
        text = quote(text)
        url = "https://www.flickr.com/search/?text=%s" % text
    else:
        url = "https://www.flickr.com/search/"
    logger.info("url: %s", url)
    try:
        response = urlopen(url)
        data = response.read().decode('utf-8')
    except:
        logger.error('url: %s', url, exc_info=True)
        return links

    # logger.info("data: %s", data)
    for line in data.splitlines():
        # logger.info("line: %s", line)

        img_data = link_pattern.search(line)
    # seems best to step through the lines
    # img_data = link_pattern.search(data)
        if img_data:
            # input('found something: %s' % img_data)
            # logger.info("img_data: %s", img_data)
            # logger.info("line: %s", line)
            link = line.split('=')[1].replace("'", '').strip(';').lower()
            ext = os.path.splitext(link)[1]
            # logger.info('ext: %s', ext)
            if ext in SUPPORTED_IMAGE_TYPES:
                links.add(link)
    logger.info("%s %s links: %s", len(links), text, links)
    return links

def download_file(url):
    if url.startswith('//'):
        url = "https:%s" % url
    # commented code loses the file name
    # (filename, headers) = urlretrieve(url)
    # logger.info('downloaded filename: %s', filename)
    filename = os.path.split(url)[1]
    data = urlopen(url)
    newfilename = '/tmp/%s' % filename
    with open(newfilename, 'wb') as newfile:
        newfile.write(data.read())
        logger.info("new file written: %s", newfilename)
        return newfilename


def function_wrapper(search_term: str):
    records = []
    logger.info("function_wrapper: %s", search_term)
    links = get_links_from_page(search_term)
    with ThreadPoolExecutor(max_workers=len(links)) as download_executor:
        download_future_results = [download_executor.submit(download_file, url) for url in links]
        for downloaded_file in as_completed(download_future_results):
            filename = downloaded_file.result()
            logger.info(filename)
            if filename:
                long = lat = None  # todo get the GPS from the new file
                record = (search_term, filename, long, lat)
                records.append(record)
    if records:
        insert_into_DB(lock, records)
        return True

if __name__ == "__main__":
    start = datetime.now()
    create_table_in_DB()
    search_terms = ('paris', 'rome', 'new york')
    with ThreadPoolExecutor(max_workers=len(search_terms)) as executor:
        search_term_future_results = [executor.submit(function_wrapper, search_term) for search_term in search_terms]
        for search_term_result in as_completed(search_term_future_results):
            logger.info(search_term_result.result())
    end = datetime.now()
    logger.info("time spent: %s", (end-start))