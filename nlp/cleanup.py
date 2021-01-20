"""
Cleanup raw text
"""
import os
import re
import string
from nltk.stem import WordNetLemmatizer
from gensim.parsing.preprocessing import remove_stopwords


def cleanup_raw_captions(caption_directory):
    data = {}
    for filename in os.listdir(caption_directory):
        if filename.endswith('.txt'):
            content = read_content(caption_directory, filename)
            content = content.lower()
            content = re.sub('[%s]' % re.escape(string.punctuation), '', content)
            content = re.sub(r'\w*\d\w*', '', content)
            content = lemmatize(content)
            content = remove_stopwords(content)
            data[filename] = content
    return data


def lemmatize(content):
    lemmatizer = WordNetLemmatizer()
    content = [lemmatizer.lemmatize(word=word, pos="v") for word in content.split(' ')]
    return ' '.join(content)


def read_content(caption_directory, filename):
    with open(os.path.join(caption_directory, filename), 'r') as f:
        return f.read()


def main():
    caption_directory = './subtitles'
    print(cleanup_raw_captions(caption_directory))


if __name__ == '__main__':
    main()
