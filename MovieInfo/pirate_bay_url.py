'''
This is to get the working piratebay url from https://proxybay.github.io/

TODO: do a status check if url is up or not (for india maybe?)
'''
from bs4 import BeautifulSoup
import requests

PIRATE_BAY_PROXY_URL = "https://proxybay.github.io/" ## this site is down, need to find another site to get pirate info from
# PIRATE_BAY_PROXY_URL = "https://github.com/okeyproxy2/Pirate-Bay-Proxy-Sites-List-Updated-Apr-2024"
PIRATE_BAY_URLS = ["https://tpirbay.xyz/", "https://tpirbay.top/","https://tpirbay.site/"]  ## Hard coding for now. 


def __get_url_from_one_row(row):
    site = row.find("td", class_="site")
    url = site.find("a", href=True)
    return url['href']


def __get_url_list_for_pirate_bay_from_rows(rows):
    urls = []
    for row in rows:
        url = __get_url_from_one_row(row)
        urls.append(url)
    return urls


def __rows_with_proxy_list():
    response = requests.request("GET", PIRATE_BAY_PROXY_URL)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    rows_with_site = soup.findChildren('table', id="proxyList")
    return rows_with_site[0]


def __get_url_list_for_pirate_bay():
    rows = __rows_with_proxy_list()
    rows = rows.findChildren(['th', 'tr'])[6:]
    return __get_url_list_for_pirate_bay_from_rows(rows)


def get_unblocked_urls_for_pirate_bay():
    """
    Parses and gets all the urls in piratebay
    """
    global PIRATE_BAY_URLS

    ## Only do it for first time to give faster responses back
    if PIRATE_BAY_URLS is None:
        urls = __get_url_list_for_pirate_bay()
        PIRATE_BAY_URLS = urls
    return PIRATE_BAY_URLS


def __add_query_to_url(url: str, msg: str):
    return url + "/search.php?q=" + msg.replace(" ", '+')


def get_msg_with_piratebay_url(msg):
    ## get top 3 urls
    pirate_bay_urls = get_unblocked_urls_for_pirate_bay()[:3]
    return_msg = "Torrent search: {0}\n Mirror Url:{1}\n Mirror Url 2:{2}".format(
        __add_query_to_url(pirate_bay_urls[0], msg), __add_query_to_url(
            pirate_bay_urls[1], msg), __add_query_to_url(pirate_bay_urls[2], msg))

    return return_msg


if __name__ == '__main__':
    ### For testing
    print(get_unblocked_urls_for_pirate_bay())
    print(get_msg_with_piratebay_url("rrr"))
