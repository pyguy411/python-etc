import json
import logging
import os
import re
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from multiprocessing import Lock
from typing import Union
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



def get_api_key():
    try:
        url = "https://www.flickr.com/search/"
        logger.info("get api key for you using url: %s", url)
        response = urlopen(url)
        data = response.read().decode('utf-8')
        re_obj = re.search("root.YUI_config.flickr.api.site_key = ", data)
        end_index = re_obj.end()
        substring = data[end_index:end_index + 50]
        logger.info(substring)
        key = substring.split(';')[0]
        key = key.replace('"', '')
        return key
    except:
        logger.error('problem getting key', exc_info=True)
        raise

def search(search_term:str=None,
           page:int=1,
           per_page: int=25,
           pages=Union[int, None],
           lock=None,
           extras:  str="geo,url_o,description",
           attempt=1,
           media:str = "photos") -> dict:
    logger.info("search_term: %s, page:%s of pages:%s, per_page: %s", search_term, page, pages, per_page)
    FLICKR_API_KEY = os.environ.get('FLICKR_API_KEY', None)
    if FLICKR_API_KEY is None:
        # do a quick search and snag it from the URL
        os.environ['FLICKR_API_KEY'] = get_api_key()

    url = "https://api.flickr.com/services/rest"
    params = {
        "method": 'flickr.photos.search',
        'text': quote(search_term),
        'per_page': per_page,
        'page': page,
        'format': 'json',
        'nojsoncallback': '1',
        'media': 'photos',
        'extras': extras,
        'api_key': os.environ['FLICKR_API_KEY']
        # content_type={{content_type}&
        # page={{page}}&
        # lang=en-US&
        # has_geo=1&
    }
    url_params = '/?' + "&".join(["%s=%s" % (k,v) for k,v in params.items()])
    url += url_params
    logger.info("url: %s", url)
    final_data = []
    with urlopen(url) as request:
        try:
            if request.getcode() != 200:
                logger.error('problem (%s:%s) with url: %s', request.getcode(),request.reason, request.url)
                return None #{'records': [], 'total': 0,
                            # 'lock': lock}
            read_data = request.read()
            data = json.loads(read_data)
        except:
            logger.error('read_data: %s', read_data, exc_info=True)
            raise
        # logger.info("json: %s", data)
        if data.get('stat') == 'ok':
            for record in data['photos']['photo']:
                try:
                    name = os.path.split(record.get('url_o'))[1]
                except:
                    name = None  #url_o is not always there. # todo decide what works just as well.
                    # logger.error('no name?: %s' ,record, exc_info=True)
                tu = (search_term, name, record.get('longitude'), record.get('latitude'))
                final_data.append(tu)
    if len(final_data) == 0:
        logger.info("no data?: attempt:%s, %s url: %s", attempt, data, url)
        if attempt == 1:
            attempt += 1
            return search(search_term=search_term,
                   page=page,
                   per_page=per_page,
                   pages=pages,
                   attempt=attempt,
                   lock=lock)
    return {'records': final_data,
            'total': data['photos']['total'],
            'url': request.url,
            'pages': data['photos']['pages'],
            'stat': data['stat'],
            'lock': lock}


def parallel_search(search_term:str=None, page: int=1, per_page: int=500):
    logger.info("parallel_search: %s", search_term)
    initial_results = search(search_term=search_term, page=page, per_page=per_page, pages=None, lock=lock)
    pages = int(initial_results['pages'])
    logger.info("search_term: %s, pages: %s", search_term, pages)
    if pages <= 1:
        return
    insert_into_DB(initial_results)
    with ThreadPoolExecutor(max_workers=200) as api_executor:
        for wanted_page in range(page+1, pages+1):
            # logger.info("search_term: %s, page: %s", search_term, page)
            api_executor.submit(search, search_term=search_term,
                                                    page=wanted_page, per_page=per_page,
                                                    pages=pages,
                                                    lock=lock).add_done_callback(insert_into_DB)
    return True


if __name__ == "__main__":
    start = datetime.now()
    create_table_in_DB()
    search_terms = ('paris', 'rome', 'new york')
    with ThreadPoolExecutor(max_workers=len(search_terms)) as executor:
        search_term_future_results = [executor.submit(parallel_search, search_term).add_done_callback(print) for search_term in search_terms]
    end = datetime.now()
    logger.info("time spent: %s", (end - start))

