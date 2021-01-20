"""
Main file
"""
from utils.config import get_config
from utils.client import get_client
from extract.search import search_youtube
from extract.caption import download_captions


def read_config():
    """
    Returns search configs.
    :param conf: conf.
    :return:
    """

    conf = get_config()
    search_text = conf['video']['search_text']
    language = conf['video']['language']
    order = conf['video']['order']
    max_results = conf['video']['max_results']
    search = conf['app']['search']
    download = conf['app']['download']
    return search_text, language, order, max_results, search, download


def main():
    """
    Main function.
    :return:
    """

    youtube = get_client()
    search_text, language, order, max_results, search, download = read_config()

    if search:
        video_ids = search_youtube(youtube, search_text, language, order, max_results)

    if download:
        download_captions(search_text, video_ids, language)


if __name__ == '__main__':
    main()
