import urllib
from urllib import parse, robotparser
from urllib.parse import urlparse

import requests


def if_robot_text_exist(url):
    session = requests.session()  # initialize the session
    domain = urllib.parse.urlparse(url).netloc
    response = session.get("http://" + domain + "/robots.txt")
    return response


def can_fetch(agent, url):
    robot_checkers = {}
    host = urlparse(url).netloc
    try:
        rc = robot_checkers[host]
    except KeyError:
        rc = robotparser.RobotFileParser()
        rc.set_url('http://' + host + '/robots.txt')
        rc.read()
        robot_checkers[host] = rc
        if agent:
            return rc.can_fetch(agent, url)
        else:
            return rc.can_fetch('*', url)


def get_site_maps(url):
    robot_checkers = {}
    host = urlparse(url).netloc
    try:
        rc = robot_checkers[host]
    except KeyError:
        rc = robotparser.RobotFileParser()
        rc.set_url('http://' + host + '/robots.txt')
        rc.read()
        robot_checkers[host] = rc
        return rc.site_maps()