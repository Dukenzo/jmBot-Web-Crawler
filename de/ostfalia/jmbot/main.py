# Author: Joseph Joel Minlo
# Ostfalia Hochschule für angewandte Wissenschaften
# Fakültät Informatik
# IT-Managment
import concurrent
import sys
import threading
import time
from argparse import ArgumentParser
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from configparser import ConfigParser
from timeit import default_timer

from de.ostfalia.jmbot.Crawler import Crawler
from de.ostfalia.jmbot.frontier.Frontier import Frontier
from de.ostfalia.jmbot.utils.Config import Config


def task(next_url, next_time, frontier, config):
    try:
        crawler = Crawler(next_url, config)
        result = crawler.crawl(threading.current_thread(), next_url, next_time, config, frontier)
        return result
    except:
        raise Exception("Exception thrown with crawler")


def main(config_file):
    # set stdout to support UTF-8
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    frontier = Frontier(config)

    for link in config.seed_urls:
        frontier.add(link)

    print("Spider %s start" % config.user_agent)
    print("%s links to crawl." % len(frontier))
    start = default_timer()
    while len(frontier.urls_to_search) > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.threads_count) as executor:
            futures = []
            while len(frontier.urls_to_search) > 0:
                try:
                    next_time, next_url = frontier.next()

                except IndexError as index_error:
                    print("Error getting next_url %s " % index_error)
                    break

                except KeyError as key_error:
                    print("Error getting next_url %s " % key_error)
                    break

                futures.append(executor.submit(task, next_url=next_url, next_time=next_time,
                                               frontier=frontier, config=config))

            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    print('%s links has been add to frontier' % len(future.result().__getitem__(0)))
                    print('%s links has been written to DB' % len(future.result().__getitem__(1)))

            print("Remaining item in frontier: %s " % len(frontier))

    end = default_timer()
    print("JmBot End within time (seconds) = " + str(end - start))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file)