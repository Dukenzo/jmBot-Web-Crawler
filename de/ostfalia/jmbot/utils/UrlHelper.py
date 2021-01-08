import re
from urllib.parse import urlparse, urljoin, urlunparse
from url_normalize import url_normalize


def is_supported_type(url):

    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        # return re.match(r".*\.(htm|html|php|jsp|jsf|asp|cgi)$", url.lower())
        return True

    except TypeError:
        print("Url scheme or type error %s ", url)
        raise


def is_valid_format(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("Url scheme error %s ", url)
        raise


def canonicalize_url(url, base):
    if url.endswith('/'):
        url = url[:-1]
    parsed = urlparse(url)
    if (parsed[1] == '' and parsed[2] != '' and not (parsed[2].startswith('/') or parsed[2].startswith('.'))) or (
            parsed[0] == '' and parsed[1] != ''):
        for i in range(len(url)):
            if url[i].isalnum():
                break
            url = 'http://' + url[i:]
            parsed = urlparse(url)
    if ':' in parsed.netloc:
        if (parsed.scheme == 'http' and parsed.netloc.split(':')[1] == '80') or (
                parsed.scheme == 'https' and parsed.netloc.split(':')[1] == '443'):
            parsed = (parsed.scheme, parsed.netloc.lower().split(':')[0], parsed.path, parsed.params, parsed.query, '')
    else:
        parsed = (parsed.scheme, parsed.netloc.lower(), parsed.path, parsed.params, parsed.query, '')
    # print(parsed)
    return urljoin(base, urlunparse(parsed))


def normalize_url(url):
    return url_normalize(url)