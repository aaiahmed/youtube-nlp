"""
Performs nlp.
"""
from nlp.create_corpus import get_clean_corpus
from nlp.create_dtm import get_dtm


def perform_nlp(search_text):
    """
    Perform nlp.
    :param search_text: search text.
    :return: dictionary containing corpus, document-term matrix.
    """
    corpus_dict = get_clean_corpus(search_text)
    dtm = get_dtm(corpus_dict)
    return corpus_dict, dtm


def main():
    """
    Main function.
    :return:
    """
    perform_nlp("apple m1")


if __name__ == '__main__':
    main()