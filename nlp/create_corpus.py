"""
Cleanup raw text
"""
import os
import re
import string
from nltk.stem import WordNetLemmatizer
from gensim.parsing.preprocessing import remove_stopwords
from utils.logger import get_logger

logger = get_logger()


def get_clean_corpus(search_text):
    """
    Returns clean corpuses.
    :param search_text: search text.
    :return: dictionary containing clean corpuses.
    """
    logger.info('Cleaning up raw text.')
    corpus_dict = {}
    caption_directory = './subtitles/' + search_text
    for filename in os.listdir(caption_directory):
        if filename.endswith('.txt'):
            content = read_content(caption_directory, filename)
            content = content.lower()
            content = re.sub('[%s]' % re.escape(string.punctuation), '', content)
            content = re.sub(r'\w*\d\w*', '', content)
            content = lemmatize(content)
            content = remove_stopwords(content)
            corpus_dict[filename] = content
    return corpus_dict


def lemmatize(content):
    """
    Lemmatizes content.
    :param content: content.
    :return:
    """
    lemmatizer = WordNetLemmatizer()
    content = [lemmatizer.lemmatize(word=word, pos="v") for word in content.split(' ')]
    return ' '.join(content)


def read_content(caption_directory, filename):
    """
    Reads given file from the target directory.
    :param caption_directory: caption directory.
    :param filename: file name.
    :return: file contents.
    """
    with open(os.path.join(caption_directory, filename), 'r') as f:
        return f.read()


def main():
    """
    Main function.
    :return:
    """
    search_text = 'cat'
    print(get_clean_corpus(search_text))


if __name__ == '__main__':
    main()
