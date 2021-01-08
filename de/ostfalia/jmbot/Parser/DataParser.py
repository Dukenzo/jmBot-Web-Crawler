# Author: Joseph Joel Minlo
# Ostfalia Hochschule für angewandte Wissenschaften
# Fakültät Informatik
# IT-Managment
import re
import sys
import time

from bs4 import BeautifulSoup

from de.ostfalia.jmbot.utils import UrlHelper
from urllib.parse import urljoin, urlparse, urldefrag


def get_links(page_url, max_pages_to_crawl, soup):
    """Returns a list of links from from this page to be crawled.
    pageurl = URL of this page
    domain = domain being crawled (None to return links to *any* domain)
    soup = BeautifulSoup object for this page
    """

    # get target URLs for all links on the page
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
        if len(links) >= max_pages_to_crawl:
            break

    # remove fragment identifiers
    links = [urldefrag(link)[0] for link in links]

    # remove any empty strings
    links = [link for link in links if link]

    # if it's a relative link, change to absolute  ['']
    links = [
        link if bool(urlparse(link).netloc) else urljoin(page_url, link)
        for link in links
    ]

    return links


def same_host(url, to_compare):
    """ return true If url are in the same host as to_compare"""
    try:
        host = urlparse(url)[2]
        host = urlparse(url)
        # urlsplit = urlsplit(url)
        return re.match(".*%s" % to_compare, host)
    except Exception as e:
        print(sys.stderr, "JmBot Url Error: Can't process url '%s' (%s)" % (url, e))
        return False


def samedomain(netloc1, netloc2):
    """Determine whether two netloc values are the same domain.
    This function does a "subdomain-insensitive" comparison. In other words ...
    samedomain('www.microsoft.com', 'microsoft.com') == True
    samedomain('google.com', 'www.google.com') == True
    samedomain('api.github.com', 'www.github.com') == True
    """
    domain1 = netloc1.lower()
    if "." in domain1:
        domain1 = domain1.split(".")[-2] + "." + domain1.split(".")[-1]

    domain2 = netloc2.lower()
    if "." in domain2:
        domain2 = domain2.split(".")[-2] + "." + domain2.split(".")[-1]

    return domain1 == domain2


class DataParser:

    @staticmethod
    def process_data(url, max_pages_to_crawl, domain, html_soup, site_map_links):

        links = []
        if html_soup:
            links = get_links(url, max_pages_to_crawl, html_soup)
        if site_map_links:
            links = site_map_links
        # links = get_links(url, html_soup)

        if links and len(links) > 0:

            # normalize urls
            links = [UrlHelper.normalize_url(link) for link in links]
            # filter by supported type
            links_for_frontier = [link for link in links if UrlHelper.is_supported_type(link)]

            # 2 Eliminate duplicate. if only crawing a single domain, remove links to other domains
            if domain:
                links_for_frontier = [link for link in links_for_frontier if
                                      not samedomain(urlparse(link).netloc, domain)]

            links_to_store = [link for link in links if samedomain(urlparse(link).netloc, domain)]

            return links_for_frontier, links_to_store
        else:
            print("NO links found")