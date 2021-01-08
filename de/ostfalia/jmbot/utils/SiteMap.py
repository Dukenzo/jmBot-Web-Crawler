from timeit import default_timer

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


def get_sitemap(url):
    get_url = requests.get(url)

    if get_url.status_code == 200:
        return get_url.text
    else:
        print('Unable to fetch sitemap: %s.' % url)
        return None


def process_sitemap(s, max_pages_to_crawl):
    soup = BeautifulSoup(s, 'lxml')
    result = []

    for loc in soup.findAll('loc'):
        result.append(loc.text)
        if len(result) >= max_pages_to_crawl:
            break
    return result


def is_sub_sitemap(url):
    parts = urlparse(url)
    if parts.path.endswith('.xml') and 'sitemap' in parts.path:
        return True
    else:
        return False


def extract_urls(sitemap_content, max_pages_to_crawl, crawling_timeout_in_seconds):
    sitemap = process_sitemap(sitemap_content, max_pages_to_crawl)
    result = []

    while sitemap:
        start_crawl_time = default_timer()
        current_sitemap = sitemap.pop()

        if is_sub_sitemap(current_sitemap):
            sub_sitemap = get_sitemap(current_sitemap)
            for i in process_sitemap(sub_sitemap, max_pages_to_crawl):
                result.append(i)
                if default_timer() - start_crawl_time > crawling_timeout_in_seconds:  # break crawl after x seconds
                    break

        else:
            result.append(current_sitemap)

        if default_timer() - start_crawl_time > crawling_timeout_in_seconds:  # break crawl after x seconds
            break

    return result