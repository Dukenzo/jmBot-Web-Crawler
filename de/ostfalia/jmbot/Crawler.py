# Author: Joseph Joel Minlo
# Ostfalia Hochschule für angewandte Wissenschaften
# Fakültät Informatik
# IT-Managment
import time
from urllib.error import URLError
from urllib.parse import urlparse

import bs4
import requests
from requests.exceptions import SSLError

from de.ostfalia.jmbot.Parser.DataParser import DataParser
from de.ostfalia.jmbot.fetcher.Fetcher import Fetcher
from de.ostfalia.jmbot.utils import jmBotDB


class Crawler:
    retry_count = None
    successfully_crawled_pages = None
    db_collection = None
    config = None
    frontier = None

    def __init__(self, config_file, frontier):

        Crawler.config = config_file
        Crawler.frontier = frontier
        Crawler.current_crawling_url = None
        Crawler.retry_mode = False
        Crawler.retry_count = 0
        Crawler.successfully_crawled_pages = 0.0
        Crawler.db_collection = jmBotDB.get_mongo_collection()

    @staticmethod
    def crawl(thread_name, next_url, next_time, config, frontier):
        print("Crawler %s start..." % thread_name)

        while time.time() < next_time:
            print("POLITNESS SLEEP")
            time.sleep(0.5)
            print("POLITNESS RESUME")

        Crawler.current_crawling_url = next_url
        # get the url domain
        domain = urlparse(next_url).netloc

        try:
            print('Crawling %s ' % next_url)
            frontier.notify_visit(next_url)
            links_for_frontier, links_to_store = None, None

            if Fetcher.robots_txt_exit(next_url):
                # crawl through sitemap
                if Fetcher.can_fetch_url(next_url):  # do this here or in the fetcher with the method below ?
                    # print('With siteMap...')
                    site_map_links = Fetcher.read_site_map(next_url, config.max_pages_to_crawl,
                                                           config.crawling_timeout)

                    links_for_frontier, links_to_store = DataParser.process_data(next_url,
                                                                                 config.max_pages_to_crawl,
                                                                                 domain, None, site_map_links)
                else:
                    print('no permission to Crawl this website')
            else:
                # crawl through DOM Document
                soup_object = Fetcher.read_html_page(next_url, config.user_agent)

                links_for_frontier, links_to_store = DataParser.process_data(next_url,
                                                                             config.max_pages_to_crawl, domain,
                                                                             soup_object, None)

            [frontier.add(link) for link in links_for_frontier]

            [Crawler.db_collection.insert_one({"url": link, "timestamp": time.time()}) for link in links_to_store]

            Crawler.successfully_crawled_pages += 1

            return links_for_frontier, links_to_store

        except URLError as error:
            print(error)
            return None
        except SSLError as ssl_error:
            print("FAILED TO RETRIEVE URL :", ssl_error)  # TODO fallback to http ?
            return None
        except requests.exceptions.ConnectTimeout as timeout:
            print("timeout RETRIEVE URL :", timeout)  # retry ?
            if Crawler.retry_count < 3:
                Crawler.retry_mode = True
                Crawler.retry_count += 1
                print("retry crawling %s ..." % Crawler.current_crawling_url)  # retry
                # TODO recall method
        except BaseException as base_exception:
            print("BaseException :", base_exception)  # can occur while fetching sitemap  example twitter
            return None
        Crawler.retry_mode = False
        Crawler.successfully_crawled_pages += 1

        print("Crawling %s end." % next_url)
        return None