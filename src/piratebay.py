from tpblite import TPB
from logger import logger
import config



def search(query):
    for proxy in config.PROXY_LIST:
        try:
            torrents = TPB(proxy).search(query)
            if torrents:
                return torrents

        except ConnectionError:
            logger.info(f"Connection Error - {proxy}")

    return None


def generate_sample_text(torrents):
    message = ''

    if len(torrents) > 2:
        sample_count = 3
    else:
        sample_count = len(torrents)

    for i in range(sample_count):
        t = torrents[i]
        message += f'- <i>{t.title}</i>\n'

    return message
