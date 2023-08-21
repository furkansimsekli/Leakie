from tpblite import TPB

import config
from logger import logger


def search(query):
    for proxy in config.PROXY_LIST:
        try:
            torrents = TPB(proxy).search(query)
            valid_torrents = []

            for torrent in torrents:
                if torrent.seeds > 50:
                    valid_torrents.append(torrent)

            if valid_torrents:
                return valid_torrents

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
