"""
Finds captions for videos.
"""
import pathlib
import youtube_dl
from xml.etree import ElementTree
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger()


def get_caption_id_using_youtube_api(youtube, video_id, language):
    """
    Find the latest caption for a video from youtube api.
    :param youtube: client.
    :param video_id: video id.
    :param language: language
    :return: caption id.
    """

    request = youtube.captions().list(
        part="id,snippet",
        videoId=video_id
    )
    response = request.execute()
    items = sorted([item for item in response['items'] if item['snippet']['language'] == language],
                   key=lambda item: item['snippet']['lastUpdated'],
                   reverse=True)
    return items[0]['id']


def download_caption_using_youtube_api(youtube, caption_id):
    """
    Find caption using youtube api.
    Requires to work around clunky google api oauth process.
    Only works for videos you own.
    :param youtube: youtube client.
    :param caption_id: caption id.
    :return:
    """
    request = youtube.captions().download(
        id=caption_id,
        tlang="en"
    )
    response = request.execute()
    print(response)


def get_caption_ids_using_youtube_api(youtube, video_ids, language):
    """
    Finds caption ids for a list of videos using youtube api.
    :param youtube: client.
    :param video_ids: list of video ids.
    :param language: language
    :return: list of caption ids.
    """

    caption_ids = []
    for video_id in video_ids:
        caption_ids.append(get_caption_id_using_youtube_api(youtube, video_id, language))
    return caption_ids


def extract_text_from_ttml(search_text, video_id):
    """
    Extracts raw text from a .ttml subtitle file.
    :param video_id: video id.
    :param search_text: search text.
    :return: raw text.
    """

    logger.info("Extracting text from raw caption.")
    text = []
    filename = 'subtitles/{search_text}/{video_id}.en.ttml'.format(search_text=search_text, video_id=video_id)
    namespace = 'http://www.w3.org/ns/ttml'
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    for item in root.findall('.//{%s}p' % namespace):
        if item.text is not None:
            text.append(item.text)
    return ' '.join(text)


def write_extracted_text(search_text, video_id, text):
    """
    Writes text to a file inside subtitles folder.
    :param search_text: search text.
    :param video_id: file name.
    :param text: raw text.
    :return:
    """

    filename = 'subtitles/{search_text}/{video_id}.txt'.format(search_text=search_text, video_id=video_id)
    with(open(filename, 'w')) as fw:
        fw.write(text)


def get_caption_using_youtube_dl(search_text, video_id, language):
    """
    Download caption using youtube-dl.
    :param search_text: search text.
    :param video_id: video id.
    :param language: language
    :return:
    """

    logger.info("Downloading caption for video id: {video_id}".format(video_id=video_id))
    pathlib.Path('subtitles/{search_text}'.format(search_text=search_text)).mkdir(parents=True, exist_ok=True)
    ydl_opts = {'writeautomaticsub': True,
                'skip_download': True,
                'subtitlesformat': 'ttml',
                'subtitleslangs': [language],
                'outtmpl': 'subtitles/{search_text}/%(id)s.%(ext)s'.format(search_text=search_text)}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_id])


def get_captions_using_youtube_dl(search_text, video_ids, language):
    """
    For a list of video ids, downloads subtitles using youtube-dl,
    extracts raw text and writes to subtitles folder.
    :param search_text:
    :param video_ids: list of video ids.
    :param language: language
    :return:
    """

    for video_id in video_ids:
        get_caption_using_youtube_dl(search_text, video_id, language)
        write_extracted_text(search_text, video_id, extract_text_from_ttml(search_text, video_id))


def download_captions(search_text, video_ids, language):
    get_captions_using_youtube_dl(search_text, video_ids, language)


def main():
    conf = get_config()
    search_text = 'apple m1'
    sample_video_ids = ['KE-hrWTgDjk']
    language = conf['video']['language']

    if conf['app']['download']:
        download_captions(search_text, sample_video_ids, language)


if __name__ == "__main__":
    main()
