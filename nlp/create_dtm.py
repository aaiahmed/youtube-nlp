"""
Converts corpuses into document-term matrix.
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def create_dataframe(corpus_dict):
    """
    Create pandas dataframe from corpuses.
    :param corpus_dict:
    :return:
    """
    return pd.DataFrame(corpus_dict.items(), columns=['filename', 'transcript'])


def get_dtm(corpus_dict):
    """
    Creates document-term matrix.
    :param corpus_dict: dictionary containing corpuses.
    :return: dtm.
    """
    df = create_dataframe(corpus_dict)
    cv = CountVectorizer(stop_words='english')
    data_cv = cv.fit_transform(df['transcript'])  # TODO: See effect of min_df, max_df, ngram_range
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = df['filename']
    return data_dtm


def main():
    """
    Main function.
    :return:
    """
    corpus = {"file1.txt": "this is a test caption"}
    print(get_dtm(corpus))


if __name__ == '__main__':
    main()
