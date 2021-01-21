"""
Performs nlp.
"""
from nlp.create_corpus import get_clean_corpus
from nlp.create_dtm import get_dtm
from nlp.create_wordcloud import show_word_cloud


def nlp(search_text):
    """
    Perform nlp.
    :param search_text: search text.
    :return:
    """
    corpus_dict = get_clean_corpus(search_text)
    dtm = get_dtm(corpus_dict)
    show_word_cloud(corpus_dict)
    print(dtm)


def main():
    """
    Main function.
    :return:
    """
    nlp("apple m1")


if __name__ == '__main__':
    main()