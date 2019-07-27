from collections import Counter
import json
import time
import logging
import requests
from threading import Thread
from textwrap import dedent
logger = logging.getLogger('flask.app')

def github_topic(owner: str, repo: str) -> list:
    """return topics list
    using https://developer.github.com/v3/repos/#list-all-topics-for-a-repository
    """
    url = "https://api.github.com/orgs/{owner}/{repo}/topics".format(owner=owner,
        repo=repo)
    resp = requests.get(url=url, verify=False)
    try:
        response_data = resp.json()
        logger.info("owner: %s, url: %s, topic json:\n%s", owner, url,
            json.dumps(response_data, indent=4))
        return response_data['names']
    except:
        logger.exception('owner: %s, url: %s', owner, url)

def github_profile(org:str):
    """- The profile should include the following information (when available):
    - Total number of public repos (seperate by original repos vs forked repos)
    - Total watcher/follower count
    - A list/count of languages used across all public repos
    - A list/count of repo topics"""

    url = "https://api.github.com/orgs/{org}/repos".format(org=org)
    resp = requests.get(url=url,
        headers= {"Accept": "application/vnd.github.mercy-preview+json"},
        verify=False)
    # logger.info("headers: %s", resp.request.headers)
    response_data = resp.json()
    logger.info("org: %s, url: %s, json:\n%s", org, url, json.dumps(response_data,
        indent=4))
    profile = {}
    profile['repos'] = repos = []
    orig_vs_forked_count = Counter()  # track original vs forked
    watchers = Counter()
    languages = []
    topics = []
    for record in response_data:
        topics.extend(record["topics"])
        language = record.get("language", '')
        if language:
            language = language.lower() # case is adding variance
        languages.append(language)
        watchers[record['name']] = record['watchers_count']
        if record["fork"] is True:
            orig_vs_forked_count['forked'] += 1
        else:
            orig_vs_forked_count['original'] += 1
        tmp_data = {
            'name': record['name'],
            "watchers_count": record['watchers_count'],
            "forks_count": record['forks_count'],
            'language': language,
            "fork": record["fork"],
            "topics": record["topics"],
            "topics_count": len(record["topics"]),
        }
        repos.append(tmp_data)
    profile['profile'] = {
        'watchers_count_per_repo': watchers,
        'total_watchers_count': sum(watchers.values()),
        'languages': Counter(languages),
        'topics': Counter(topics),
        'orig_vs_forked_count': orig_vs_forked_count,
    }
    logger.debug("profile data: \n%s", json.dumps(profile, indent=2))
    return profile

def bitbucket_meta_size(org: str=None, repo:str=None , meta: str=None,
                        url: str=None,
                        data: dict=None) -> int:
    """if url is given, use that.
    otherwise, construct it.
    """
    if url is None:
        url = "https://api.bitbucket.com/2.0/repositories/{org}/{repo}/{meta}".format(
        org=org, repo=repo, meta=meta)
    resp = requests.get(url=url, verify=False)
    response_data = resp.json()
    # logger.info('url %s, meta: %s, json: %s', url, meta,
    #     json.dumps(response_data, indent=4))
    if not data:
        return response_data['size']
    else:
        data['{}_count'.format(meta)] = response_data['size']

def bitbucket_profile(org: str) -> dict:
    """org - the organization entity
    - The profile should include the following information (when available):
        - Total number of public repos (seperate by original repos vs forked repos) - NOT AVAILABLE to see when forked
        - Total watcher/follower count
        - A list/count of languages used across all public repos
        - A list/count of repo topics - NOT AVAILABLE
    """

    records = [] # iterate across these after we have stepped through all pages.
    url = "https://api.bitbucket.com/2.0/repositories/{org}".format(org=org)
    resp = requests.get(url=url, verify=False)
    response_data = resp.json()
    logger.info("org: %s, url: %s, json:\n%s", org, url, json.dumps(
        response_data, indent=4))
    profile = {}
    profile['repos'] = repos = []
    watchers = Counter()
    languages = []
    records.extend(response_data['values'])
    going_back_for_more_counter = 0
    while response_data.get('next'):
        going_back_for_more_counter += 1
        url = response_data.get('next')
        resp = requests.get(url=url, verify=False)
        response_data = resp.json()
        logger.info("org: %s, counter: %s, url: %s, json:\n%s", org,
            going_back_for_more_counter, url, json.dumps(
            response_data, indent=4))
        records.extend(response_data['values'])
    threads = []
    for idx, record in enumerate(records, 1):
        logger.debug("record %s of %s", idx, len(records))
        language = record.get("language", '')
        if language:
            language = language.lower()
        languages.append(language)
        tmp_data = {
            'name': record['name'],
            'language': language,
        }
        # "watchers_count": bitbucket_meta_size(
        #     url=record['links' ]['watchers']['href']),
        # "forks_count": bitbucket_meta_size(
        #     url=record['links']['forks']['href']),
        watchers_thread = Thread(target=bitbucket_meta_size,
            name='{}-{}-watchers'.format(idx,record['name']),
            kwargs={
            "meta": "watchers",
            "url": record['links']['watchers']['href'],
            'data': tmp_data}
        )
        watchers_thread.start()
        threads.append(watchers_thread)
        forks_thread = Thread(target=bitbucket_meta_size,
            name='{}-{}-forks'.format(idx, record['name']),
            kwargs={
            "meta": "forks",
            "url": record['links']['forks']['href'],
            'data': tmp_data}
        )
        forks_thread.start()
        threads.append(forks_thread)
        repos.append(tmp_data)
    while any([i.is_alive() for i in threads]):
        logger.info("active threads: %s", [i.name for i in threads if i.is_alive])
        time.sleep(1)
    for tmp_data in repos:
        watchers[tmp_data['name']] = tmp_data['watchers_count']
    profile['profile'] = {
        'watchers_count_per_repo': watchers,
        'total_watchers_count': sum(watchers.values()),
        'languages': Counter(languages),
        'topics': 'Not Available',
        'repo_count': response_data['size'],
    }
    logger.debug("profile data: \n%s", json.dumps(profile, indent=2))
    return profile

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG,
        filename='fetch.log',
        # filemode='a'
        filemode='w'
        )
    logger = logging.getLogger()
    start = time.time()
    # bitbucket_profile('pygame')
    bitbucket_profile('mailchimp')
    # bitbucket_profile('microsoft')
    # github_profile('pygame')
    # github_profile('mailchimp')
    end = time.time()
    logger.info("time to complete: %s", end-start)
