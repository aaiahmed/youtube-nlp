"""
Main file
"""
from utils.config import get_config
from utils.client import get_client
from extract.search import search_youtube
from extract.caption import download_captions
from nlp.perform_nlp import perform_nlp
from demo.create_wordcloud import show_word_cloud


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
    nlp = conf['app']['nlp']
    return search_text, language, order, max_results, search, download, nlp


def main():
    """
    Main function.
    :return:
    """

    youtube = get_client()
    search_text, language, order, max_results, search, download, nlp = read_config()

    if search:
        video_ids = search_youtube(youtube, search_text, language, order, max_results)

    if download:
        download_captions(search_text, video_ids, language)

    if nlp:
        corpus_dict, dtm = perform_nlp(search_text)
        show_word_cloud(corpus_dict)


if __name__ == '__main__':
    main()
