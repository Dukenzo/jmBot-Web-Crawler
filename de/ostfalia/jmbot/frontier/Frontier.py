# Author: Joseph Joel Minlo
# Ostfalia Hochschule für angewandte Wissenschaften
# Fakültät Informatik
# IT-Managment


# store links to be visit
# decide which url will be processes nex
# selected url respect following policies: page quality, page update, efficient resource allocation
import heapq
import time
from urllib.parse import urlparse


class Frontier(object):
    def __init__(self, config):

        # A list of urls that still have to be searched sorted by
        # domains
        self.urls_to_search = {}

        # A list containing the next crawltimes on domain level,
        # to achieve a optimal throughput maintaining a polite policy
        self.crawltimes = []

        # Urls we have already found and in our set
        self.founded_urls = set()

        # must be configurable
        self._polite_time = config.time_delay

    @property
    def polite_time(self):
        return self._polite_time

    @property
    def founded_urls_(self):
        return self.founded_urls

    @polite_time.setter
    def polite_time(self, seconds):
        if seconds >= 0:
            self._polite_time = seconds

    def add(self, link):
        # print("Add to frontier: %s" % url)
        if link in self.founded_urls:
            return False

        domain = urlparse(link).netloc

        # means this is the first URL in our set
        # also set the refresh frequenz for this domain
        if not domain in self.urls_to_search:
            self.urls_to_search[domain] = []
            heapq.heappush(self.crawltimes, (time.time(), domain))

        self.urls_to_search[domain].append(link)
        self.founded_urls.add(link)
        return True

    def delete(self, link):

        domain = urlparse(link).netloc
        del (self.urls_to_search[domain])

        return True

    def next(self):
        next_time, next_domain = heapq.heappop(self.crawltimes)

        next_url = self.urls_to_search[next_domain].pop()

        if len(self.urls_to_search[next_domain]) == 0:
            del (self.urls_to_search[next_domain])

        return next_time, next_url

    def notify_visit(self, url):
        domain = urlparse(url).netloc

        # If there are still other urls on this domain to crawl, add crawl time
        if domain in self.urls_to_search:
            heapq.heappush(self.crawltimes, (time.time() + self.polite_time, domain))

    def __len__(self):
        return sum([len(self.urls_to_search[domain]) for domain in self.urls_to_search])