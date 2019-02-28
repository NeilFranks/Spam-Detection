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

"""
    Deletes common words from the English dictionary.
    Also deletes words that are not alphabetical or of the length <= 2
    
    Not quite sure whether to include numbers or not.
    
    Neil: I think we might want to allow non-alpha words. Im seeing stuff like "???", "000000", "000" common for spam
"""
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
                      "too", "very", "can", "will", "just", "don", "should", "now", "nbsp"]

def remove_common_words(dict):
    words = list(dict.keys())
    for word in words:
        if word in commonWordList:
            del(dict[word])
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

def read_emails_from_directory(directory):
    emailList = []
    for file in os.listdir(directory):
        emailList.append(os.path.join(directory, file))

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
            if word[0] == "Subject:":
                currentSubjectListOfWords += word
            else:
                currentBodyListOfWords += word

        # to keep track of phrases, I'll use a list that acts like a queue
        current2Word = ["", ""]
        current3Word = ["", "", ""]

        """
        Get phrases for body
        """
        # listOfWords contains words seen in order in the email
        # Increment through all of them and keep track of phrases
        for word in currentBodyListOfWords:
            if word.isalpha() and word not in commonWordList:

                #update current phrase seen
                current2Word[0] = current2Word[1]
                current2Word[1] = word

                current3Word[0] = current3Word[1]
                current3Word[1] = current3Word[2]
                current3Word[2] = word

                #add the words to listOfPhrases as a single string, with a space between them
                bodyListOfPhrases.append(current2Word[0] + " " + current2Word[1])
                bodyListOfPhrases.append(current3Word[0] + " " + current3Word[1] + " " + current3Word[2])

        """
        Get phrases for subject
        """
        # listOfWords contains words seen in order in the email
        # Increment through all of them and keep track of phrases
        for word in currentSubjectListOfWords:
            if word.isalpha() and word not in commonWordList:
                # update current phrase seen
                current2Word[0] = current2Word[1]
                current2Word[1] = word

                current3Word[0] = current3Word[1]
                current3Word[1] = current3Word[2]
                current3Word[2] = word

                # add the words to listOfPhrases as a single string, with a space between them
                subjectListOfPhrases.append(current2Word[0] + " " + current2Word[1])
                subjectListOfPhrases.append(current3Word[0] + " " + current3Word[1] + " " + current3Word[2])


        bodyListOfWords += currentBodyListOfWords
        subjectListOfWords += currentSubjectListOfWords


    bodyWordFrequency = collections.Counter(bodyListOfWords)
    bodyWordFrequency = remove_common_words(bodyWordFrequency)

    subjectWordFrequency = collections.Counter(subjectListOfWords)
    subjectWordFrequency = remove_common_words(subjectWordFrequency)

    bodyPhraseFrequency = collections.Counter(bodyListOfPhrases)

    subjectPhraseFrequency = collections.Counter(subjectListOfPhrases)


    return bodyWordFrequency.most_common(500), subjectWordFrequency.most_common(500), bodyPhraseFrequency.most_common(500), subjectPhraseFrequency.most_common(500)

if __name__ == "__main__":
    print('Enter directory: ')
    directory = input()
    result = read_emails_from_directory(directory)
    print("body words:", result[0])
    print("subject words:", result[1])
    print("body phrases:", result[2])
    print("subject phrases:", result[3])

    # directory input:
    #   C:\Users\Brad\PycharmProjects\EmailReader\spam
    # which I got from;
    #   http://www2.aueb.gr/users/ion/data/enron-spam/

    # Output Example:
    # ... ('these', 330), ('free', 314), ('within', 313), ('pills', 311), ('size', 306) ...




