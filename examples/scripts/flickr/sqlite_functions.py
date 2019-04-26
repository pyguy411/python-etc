import logging
import sqlite3
from concurrent.futures import Future
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

DATABASE_FILENAME = 'flickr.images.sq3'

def insert_into_DB(future_result:Union[dict,Future]):
    if isinstance(future_result, (dict,)):
        result = future_result
    else:
        result = future_result.result()
    lock = result['lock']
    lock.acquire()
    data = result['records']
    # logger.info("lock acquired.")
    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()
    record_count = len(data)
    logger.info("inserting %s records", record_count)
    if record_count == 0:
        lock.release()
        logger.info("no results? stat: %s, url: '%s' ", result.get('stat'), result['url'])
        return
    elif record_count == 1:
        cursor.execute("INSERT INTO IMAGES VALUES (?,?,?,?)", data)
    else:
        cursor.executemany("INSERT INTO IMAGES VALUES (?,?,?,?)", data)
    conn.commit()
    lock.release()
    # logger.info("lock released.")

def create_table_in_DB():
    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS IMAGES (search_term text, name text, long text, lat text)""")
