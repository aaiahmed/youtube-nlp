"""
Find most commonly used words in caption.
"""
import pandas as pd


def find_top_words(dtm):
    """
    Find top words from document-term matrix.
    :param dtm: dtm.
    :return:
    """
    dtm = dtm.transpose()
    top_dict = {}
    for col in dtm.columns:
        top = dtm[col].sort_values(ascending=False).head(20)
        top_dict[col]= list(zip(top.index, top.values))
    print(top_dict)


def main():
    """
    Main function.
    :return:
    """
    dict = {'filename': ['a.txt', 'b.txt'],
            'first_word': [0, 1],
            'second_word': [1, 0]}
    dtm = pd.DataFrame(dict, columns=['filename', 'first_word', 'second_word'])
    dtm.set_index('filename', inplace=True)
    find_top_words(dtm)


if __name__ == '__main__':
    main()
