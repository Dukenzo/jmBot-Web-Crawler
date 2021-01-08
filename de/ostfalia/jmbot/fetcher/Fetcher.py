# Author: Joseph Joel Minlo
# Ostfalia Hochschule für angewandte Wissenschaften
# Fakültät Informatik
# IT-Managment

import bs4
import requests

from de.ostfalia.jmbot.utils import Robots, SiteMap


class Fetcher:

    @staticmethod
    def read_site_map(url, max_pages_to_crawl, crawling_timeout):
        # TODO call dns resolver to get ip url ans pass ip to the bottom function in place of url.

        # try to get all links from site_map
        site_maps = Robots.get_site_maps(url)  # // TODO check this return value for iterable
        if site_maps:
            page_links = []
            for site_map in site_maps:
                page_links.extend(SiteMap.extract_urls(SiteMap.get_sitemap(site_map),
                                                       max_pages_to_crawl, crawling_timeout))

            return page_links
        else:
            return []

    @staticmethod
    def read_html_page(url, user_agent):
        return get_soup_html_page(url, user_agent)

    @staticmethod
    def robots_txt_exit(url):
        return Robots.if_robot_text_exist(url)

    @staticmethod
    def can_fetch_url(url):
        return Robots.can_fetch(None, url)


def get_soup_html_page(url, user_agent):
    # ip = self.dns_resolver.get_url_ip(url)
    session = requests.session()  # initialize the session
    session.headers = {'User-Agent': user_agent}

    try:
        response = session.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
            requests.exceptions.TooManyRedirects, requests.exceptions.SSLError):
        raise print("FAILED TO RETRIEVE URL :", url)

    if not response.headers["content-type"].startswith("text/html"):
        raise print("Skip data because no html.")  # don't crawl non-HTML content

        # Note that we create the Beautiful Soup object here (once) and pass it
        # to the other functions that need to use it
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return soup