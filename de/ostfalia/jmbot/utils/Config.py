import re


class Config(object):
    def __init__(self, config):
        self.user_agent = config["JMBOT_IDENT"]["USERAGENT"].strip()
        assert self.user_agent == "JmBot", "Set useragent in config.ini"
        assert re.match(r"^[a-zA-Z0-9_ ,]+$", self.user_agent), "User agent should not have any special characters outside '_', ',' and 'space'"
        self.threads_count = int(config["JMBOT_PROPERTIES"]["THREADCOUNT"])

        self.host = config["CONNECTION"]["HOST"]
        self.port = int(config["CONNECTION"]["PORT"])

        self.seed_urls = config["CRAWLER"]["SEEDURLS"].split(",")
        self.time_delay = float(config["CRAWLER"]["POLITENESS"])
        self.max_pages_to_crawl = float(config["CRAWLER"]["MAX_PAGES_TO_CRAWL"])
        self.crawling_timeout = float(config["CRAWLER"]["CRAWLING_TIMEOUT"])

        self.cache_server = None