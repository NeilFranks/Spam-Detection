import os
import collections
import tkinter
from tkinter import filedialog


class CommonCounter:

    _commonWordList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                      "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                      "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                      "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
                      "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but",
                      "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                      "against", "between", "into", "through", "during", "before", "after", "above", "below", "to",
                      "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                      "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                      "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                      "too", "very", "can", "will", "just", "should", "now", "nbsp"]

    def __init__(self, n):
        self._words = []
        self._phrases2 = []
        self._phrases3 = []
        return

    def remove_common_words(self, dict):
        words = list(dict.keys())
        for word in words:
            if word in self._commonWordList:
                del (dict[word])
            elif len(word) <= 2:
                del (dict[word])
            # elif not word.isalpha():
            #     del (dict[word])

        # if you don't remove non-alpha words, "Subject:" becomes super common, since it keeps reading the subject for every email
        del (dict["Subject:"])

        return dict