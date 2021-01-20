"""
Searches in youtube for given text.
"""

from utils.config import get_config
from utils.client import get_client
from utils.logger import get_logger

logger = get_logger()


def search_youtube(youtube, search_text, language, order, max_results):
    """
    Searches desired text in youtube api and returns result.
    :param youtube: youtube client.
    :param search_text: text to search in youtube.
    :param language: desired caption language.
    :param order: define search order.
    :param max_results: limit of number of videos.
    :return: a list containing video ids.
    """

    logger.info("Searing youtube for: {search_text}".format(search_text=search_text))
    request = youtube.search().list(
        q=search_text,
        order=order,
        part="snippet",
        type="video",
        relevanceLanguage=language,
        videoCaption="closedCaption",
        maxResults=max_results
    )

    response = request.execute()
    return [item['id']['videoId'] for item in response['items']]


def main():
    conf = get_config()
    youtube = get_client()

    search_text = conf['video']['search_text']
    language = conf['video']['language']
    order = conf['video']['order']
    max_results = conf['video']['max_results']

    if conf['app']['search']:
        print(search_youtube(youtube, search_text, language, order, max_results))


if __name__ == "__main__":
    main()
