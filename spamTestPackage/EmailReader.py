#
# Brad Duszynski
# 2-27-19
#

'''
    Simple functions that append all files in a directory into
    a list. It also iterates through each email word by word to get
    all words. It then uses collections.Counter to get the count of
    each word, and removes common words.
    TODO: combine functionality with Neil's code to do the same directly from emails
'''

import os
import collections
import tkinter
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from tkinter import filedialog

"""
    Deletes common words from the English dictionary.
    Also deletes words that are not alphabetical or of the length <= 2
    Not quite sure whether to include numbers or not.
    Neil: I think we might want to allow non-alpha words. Im seeing stuff like "???", "000000", "000" common for spam
"""


class EmailReader:
    commonWordList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                      "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                      "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                      "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
                      "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but",
                      "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                      "against", "between", "into", "through", "during", "before", "after", "above", "below", "to",
                      "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                      "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                      "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                      "too", "very", "can", "will", "just", "don", "should", "now", "nbsp", "enron"]

    def __init__(self):
        return

    def remove_common_words(self, dict):
        words = list(dict.keys())
        for word in words:
            if word in self.commonWordList:
                del (dict[word])
            elif len(word) <= 2:
                del (dict[word])
            # elif not word.isalpha():
            #     del (dict[word])

        # if you don't remove non-alpha words, "Subject:" becomes super common, since it keeps reading the subject for every email
        del (dict["Subject:"])

        return dict

    '''
        Simple solution to iterate through a directory and append
        all .txt files to a list.
        Great documentation here:
        https://www.tutorialspoint.com/python3/os_listdir.htm
        and here:
        https://docs.python.org/3/library/os.path.html#os.path.join

        Goes through each document word by word and adds them 
        to a list (listOfWords)

        Then it finally utilizes Counter to put it into a dictionary
        that counts frequency of words and comes with a handy 
        "most_common" feature.

        At this point I'm not sure how many words to return
        so I'm returning 500. It might be too much or too little, 
        but we'll see once we expand it to machine learning.

        Neil: I'm trying to make listOfPhrases contain 2 and 3 word phrases.
        Will choose them indiscriminantly; just any 2 or 3 words that occur in a row
    '''

    def read_emails_from_directory(self, directory):
        emailList = []
        # Opens all files (including folders in files)
        for (path, _, files) in os.walk(directory):
            for file in files:
                # if file.endswith('.txt'):  # not necessary but just is a safety measure
                emailList.append(os.path.join(path, file))

        bodyListOfWords = []
        subjectListOfWords = []
        bodyListOfPhrases = []
        subjectListOfPhrases = []
        for email in emailList:

            current = open(email, encoding='latin-1')
            lines = current.readlines()

            currentBodyListOfWords = []
            currentSubjectListOfWords = []

            for i in lines:
                # note: word is actually a list of all words in the line
                word = i.split()
                # check that word is not an empty list
                if word:
                    if word[0] == "Subject:":
                        currentSubjectListOfWords += word
                    else:
                        currentBodyListOfWords += word

            # to keep track of phrases, I'll use a list that acts like a queue
            current2Word = ["", ""]
            current3Word = ["", "", ""]
            current4Word = ["", "", "", ""]
            current5Word = ["", "", "", "", ""]

            """
            Get phrases for body
            """
            # listOfWords contains words seen in order in the email
            # Increment through all of them and keep track of phrases
            for word in currentBodyListOfWords:
                if word.isalpha() and word not in self.commonWordList:
                    # update current phrase seen
                    current2Word[0] = current2Word[1]
                    current2Word[1] = word

                    current3Word[0] = current3Word[1]
                    current3Word[1] = current3Word[2]
                    current3Word[2] = word

                    # add the words to listOfPhrases as a single string, with a space between them
                    bodyListOfPhrases.append(current2Word[0] + " " + current2Word[1])
                    bodyListOfPhrases.append(current3Word[0] + " " + current3Word[1] + " " + current3Word[2])

            """
            Get phrases for subject
            """

            """
            Note: It is interesting storing the phrases after removing stop words. Therefore, any phrase of 3 or 4 stopwords
            followed by a not stopword becomes the same. So I'm seeing ('   prescription ', 7) as a reflection that there were
            7 instances of 3 stopwords, then prescription, then a stop word.

            We should test whether it is better to remove the stop words before or after storing the phrase.
            """
            # listOfWords contains words seen in order in the email
            # Increment through all of them and keep track of phrases
            for word in currentSubjectListOfWords:
                if word.isalpha() and word not in self.commonWordList:
                    # update current phrase seen
                    current2Word[0] = current2Word[1]
                    current2Word[1] = word

                    current3Word[0] = current3Word[1]
                    current3Word[1] = current3Word[2]
                    current3Word[2] = word

                    current4Word[0] = current4Word[1]
                    current4Word[1] = current4Word[2]
                    current4Word[2] = current4Word[3]
                    current4Word[3] = word

                    current5Word[0] = current5Word[1]
                    current5Word[1] = current5Word[2]
                    current5Word[2] = current5Word[3]
                    current5Word[3] = current5Word[4]
                    current5Word[4] = word

                    # add the words to listOfPhrases as a single string, with a space between them
                    subjectListOfPhrases.append(current2Word[0] + " " + current2Word[1])
                    subjectListOfPhrases.append(current3Word[0] + " " + current3Word[1] + " " + current3Word[2])
                    subjectListOfPhrases.append(current4Word[0] + " " + current4Word[1] + " " + current4Word[2]
                                                + " " + current4Word[3])
                    subjectListOfPhrases.append(current5Word[0] + " " + current5Word[1] + " " + current5Word[2]
                                                + " " + current5Word[3] + " " + current5Word[4])

            bodyListOfWords += currentBodyListOfWords
            subjectListOfWords += currentSubjectListOfWords

        bodyWordFrequency = collections.Counter(bodyListOfWords)
        bodyWordFrequency = self.remove_common_words(bodyWordFrequency)

        subjectWordFrequency = collections.Counter(subjectListOfWords)
        subjectWordFrequency = self.remove_common_words(subjectWordFrequency)

        bodyPhraseFrequency = collections.Counter(bodyListOfPhrases)

        subjectPhraseFrequency = collections.Counter(subjectListOfPhrases)

        return bodyWordFrequency.most_common(3000), subjectWordFrequency.most_common(
            3000), bodyPhraseFrequency.most_common(
            3000), subjectPhraseFrequency.most_common(3000)

    def extract_features(self, mail_dir, dictionary):
        files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
        features_matrix = np.zeros((len(files), 3000))
        docID = 0
        for fil in files:
            with open(fil, encoding="latin-1") as fi:
                for i, line in enumerate(fi):
                    words = line.split()
                    if words[0] != "Subject:" and words[0] != "Subject":
                        for word in words:
                            for j, d in enumerate(dictionary):
                                if d[0] == word:
                                    wordID = j
                                    features_matrix[docID, wordID] = words.count(word)
            docID = docID + 1
        return features_matrix

    # Same Extration process, just instead gets the email_list of the
    # inbox. Doesn't incorporate subject line yet.
    def extract_features_from_email(self, email_list, dictionary):
        features_matrix = np.zeros((len(email_list), 3000))
        emailID = 0
        for email in email_list:
            lines = email.get_subject()
            lines += "\n"
            lines += email.get_body()
            if isinstance(lines, str):
                words = lines.split()
                if len(words) != 0 and (words[0] != "Subject:" and words[0] != "Subject"):
                    for word in words:
                        for j, d in enumerate(dictionary):
                            if d[0] == word:
                                wordID = j
                                features_matrix[emailID, wordID] = words.count(word)
            emailID = emailID + 1
        return features_matrix

    def get_result(self):
        # file opener
        tkinter.Tk().withdraw()
        directory = filedialog.askdirectory()
        result = self.read_emails_from_directory(directory)

        train_labels = np.zeros(1430)
        train_labels[715:1430] = 1
        # This equates to 1-715 = HAM and 716-1430 = SPAM
        #                              If you change result[n] to something else
        #                              Make sure you change the same result down
        #                              down in line 251 (test_matrix)
        train_matrix = self.extract_features(directory, result[0])
        #print(train_matrix)
        # print("body words:", result[0])
        # print("\n\nsubject words:", result[1])
        # print("\n\nbody phrases:", result[2])
        # print("\n\nsubject phrases:", result[3])

        print("body words:", len(result[0]))
        print("subject words:", len(result[1]))
        print("body phrases:", len(result[2]))
        print("subject phrases:", len(result[3]))

        model1 = MultinomialNB()
        model2 = LinearSVC()
        model3 = RandomForestClassifier()
        model4 = KNeighborsClassifier()
        model1.fit(train_matrix, train_labels)
        model2.fit(train_matrix, train_labels)
        model3.fit(train_matrix, train_labels)
        model4.fit(train_matrix, train_labels)

        test_dir = filedialog.askdirectory()
        #                                       Here -----v
        test_matrix = self.extract_features(test_dir, result[0])
        test_labels = np.zeros(600)
        # This equates to 1-300 = HAM and 301-600 = SPAM
        test_labels[300:600] = 1
        result1 = model1.predict(test_matrix)
        result2 = model2.predict(test_matrix)
        result3 = model3.predict(test_matrix)
        result4 = model4.predict(test_matrix)

        print(confusion_matrix(test_labels, result1))
        print(confusion_matrix(test_labels, result2))
        print(confusion_matrix(test_labels, result3))
        print(confusion_matrix(test_labels, result4))
        return result

    #
    #   Make sure when you use this, you input the training set
    #   I posted on slack.
    #
    def get_result_from_emails(self, email_list):
        # file opener
        tkinter.Tk().withdraw()
        directory = filedialog.askdirectory()
        result = self.read_emails_from_directory(directory)

        train_labels = np.zeros(1430)
        train_labels[715:1430] = 1
        # This equates to 1-715 = HAM and 716-1430 = SPAM
        #                              If you change result[n] to something else
        #                              Make sure you change the same result down
        #                              down in line 251 (test_matrix)
        train_matrix = self.extract_features(directory, result[0])

        print("body words:", len(result[0]))
        print("subject words:", len(result[1]))
        print("body phrases:", len(result[2]))
        print("subject phrases:", len(result[3]))

        model = LinearSVC()
        model.fit(train_matrix, train_labels)

        # develop test matrix from emails in inbox
        test_matrix = self.extract_features_from_email(email_list, result[0])
        # predict with training model from enron
        result = model.predict(test_matrix)
        return result


if __name__ == '__main__':
    a = EmailReader()
    a.get_result()
    # directory input:
    #   C:\Users\Brad\PycharmProjects\EmailReader\spam
    # which I got from;
    #   http://www2.aueb.gr/users/ion/data/enron-spam/

    # Output Example:
    # ... ('these', 330), ('free', 314), ('within', 313), ('pills', 311), ('size', 306) ...
