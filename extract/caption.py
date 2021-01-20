"""
Finds captions for videos.
"""
import youtube_dl
from xml.etree import ElementTree
from utils.config import get_config


def get_captions_using_youtube_dl(video_ids, language):
    """
    For a list of video ids, downloads subtitles using youtube-dl,
    extracts raw text and writes to subtitles folder.
    :param video_ids: list of video ids.
    :param language: language
    :return:
    """

    for video_id in video_ids:
        get_caption_using_youtube_dl(video_id, language)
        write_extracted_text(video_id, extract_text_from_ttml(video_id))


def get_caption_using_youtube_dl(video_id, language):
    """
    Download caption using youtube-dl.
    :param video_id: video id.
    :return:
    """

    ydl_opts = {'writeautomaticsub': True,
                'skip_download': True,
                'subtitlesformat': 'ttml',
                'subtitleslangs': [language],
                'outtmpl': 'subtitles/%(id)s.%(ext)s'}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_id])


def extract_text_from_ttml(video_id):
    """
    Extracts raw text from a .ttml subtitle file.
    :param file: source file.
    :return: raw text.
    """

    text = []
    filename = 'subtitles/{video_id}.en.ttml'.format(video_id=video_id)
    namespace = 'http://www.w3.org/ns/ttml'
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    for item in root.findall('.//{%s}p' % namespace):
        text.append(item.text)
    return ' '.join(text)


def write_extracted_text(video_id, text):
    """
    Writes text to a file inside subtitles folder.
    :param video_id: file name.
    :param text: raw text.
    :return:
    """

    filename = 'subtitles/{video_id}.txt'.format(video_id=video_id)
    with(open(filename, 'w')) as fw:
        fw.write(text)


def get_caption_ids_using_youtube_api(youtube, video_ids, language):
    """
    Finds caption ids for a list of videos using youtube api.
    :param youtube: client.
    :param video_ids: list of video ids.
    :return: list of caption ids.
    """

    caption_ids = []
    for video_id in video_ids:
        caption_ids.append(get_caption_id_using_youtube_api(youtube, video_id, language))
    return caption_ids


def get_caption_id_using_youtube_api(youtube, video_id, language):
    """
    Find the latest caption for a video from youtube api.
    :param youtube: client.
    :param video_id: video id.
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


def main():
    conf = get_config()
    sample_video_ids = ['o_-HIxXRfOY']
    language = conf['video']['language']

    if conf['app']['download']:
        get_captions_using_youtube_dl(sample_video_ids, language)


if __name__ == "__main__":
    main()
