import os
import collections
import tkinter
from tkinter import filedialog


class CommonCounter:

    _stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
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

    """
    You will have a separate CommonCounter object for subject and body
    part is a string, either "body" or "subject"
    """
    def __init__(self, part):
        self._part = part
        self._words = []
        self._phrases2 = []
        self._phrases3 = []
        self._phrases4 = []
        self._phrases5 = []
        return

    """
    email list is a list of the class Email.py.
    n is the number of most common returned
    """
    def get_common(self, email_list, n):
        for email in email_list:

            if self._part == "subject":
                lines = email.get_subject()
            elif self._part == "body":
                lines = email.get_body()

            if isinstance(lines, str):
                # note: word is actually a list of all words in the line
                words = lines.split()

                # add all words to list of words. Don't consider stop words here
                self._words += words
            else:
                for i in lines:
                    # note: word is actually a list of all words in the line
                    words = i.split()

                    # add all words to list of words. Don't consider stop words here
                    self._words += words


            # parse phrases after getting every word in the email

            current_2_word = ["", ""]
            current_3_word = ["", "", ""]
            current_4_word = ["", "", "", ""]
            current_5_word = ["", "", "", "", ""]

            for word in words:
                # update current phrase seen
                current_2_word[0] = current_2_word[1]
                current_2_word[1] = word

                current_3_word[0] = current_3_word[1]
                current_3_word[1] = current_3_word[2]
                current_3_word[2] = word

                current_4_word[0] = current_4_word[1]
                current_4_word[1] = current_4_word[2]
                current_4_word[2] = current_4_word[3]
                current_4_word[3] = word

                current_5_word[0] = current_5_word[1]
                current_5_word[1] = current_5_word[2]
                current_5_word[2] = current_5_word[3]
                current_5_word[3] = current_5_word[4]
                current_5_word[4] = word

                self.append_phrases(current_2_word, current_3_word, current_4_word, current_5_word)

            # remove stopwords now
            self._words = self.remove_stop_words(self._words)
            self._phrases2 = self.remove_stop_words(self._phrases2)
            self._phrases3 = self.remove_stop_words(self._phrases3)
            self._phrases4 = self.remove_stop_words(self._phrases4)
            self._phrases5 = self.remove_stop_words(self._phrases5)

            # sort by most common
            freq1 = collections.Counter(self._words)
            freq2 = collections.Counter(self._phrases2)
            freq3 = collections.Counter(self._phrases3)
            freq4 = collections.Counter(self._phrases4)
            freq5 = collections.Counter(self._phrases5)


        return freq1.most_common(n), freq2.most_common(n), freq3.most_common(n), freq4.most_common(n), freq5.most_common(n)


    def append_phrases(self, current_2_word, current_3_word, current_4_word, current_5_word):
        # don't add the phrases if the first (or more) elements are empty string
        if current_2_word[0] != "":
            self._phrases2.append(current_2_word[0] + " " + current_2_word[1])
        if current_3_word[0] != "":
            self._phrases3.append(current_3_word[0] + " " + current_3_word[1] + " " + current_3_word[2])
        if current_4_word[0] != "":
            self._phrases4.append(current_4_word[0] + " " + current_4_word[1] + " " + current_4_word[2] + " "
                              + current_4_word[3])
        if current_5_word[0] != "":
            self._phrases5.append(
            current_5_word[0] + " " + current_5_word[1] + " " + current_5_word[2] + " " + current_5_word[3]
            + " " + current_5_word[4])

    """
    list can be list of words or phrases
    """
    def remove_stop_words(self, list):
        newList = []

        if list:
            if isinstance(list[0], str):
                # list is list of individual words
                for word in list:
                    if word not in self._stop_words:
                        newList.append(word)
            else:
                # list is list of phrases
                    for phrase in list:
                        newPhrase = []
                        for word in phrase:
                            if word not in self._stop_words:
                                newPhrase.append(word)
                            else:
                                newPhrase.append("_") # append a blank in place of the stop word
                        newList.append(newPhrase)

        return newList
