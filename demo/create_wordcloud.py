"""
Creates wordcloud from corpuses dictionary.
"""

import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction import text


def show_word_cloud(corpus_dict):
    """
    Generate and show word cloud from corpuses dictionary.
    :param corpus_dict: dictionary containing corpuses.
    :return:
    """
    stop_words = text.ENGLISH_STOP_WORDS
    wc = WordCloud(stopwords=stop_words,
                   background_color="white",
                   colormap="Dark2",
                   max_font_size=100)

    fig, ax = plt.subplots()
    for index, (item, value) in enumerate(corpus_dict.items()):
        wc.generate(corpus_dict[item])
        plt.subplot(3, 4, index+1)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(item)
    st.pyplot(fig)


def main():
    """
    Main function.
    :return:
    """
    corpus = {"file1.txt": "this is a test caption"}
    show_word_cloud(corpus)


if __name__ == '__main__':
    main()