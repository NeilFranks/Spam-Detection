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
"""

def remove_common_words(dict):
    commonWordList = ['the', 'be', 'to', 'of', 'and', 'in', 'that', 'have', 'it', 'for', 'not', 'on',
                      'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'by', 'from', 'your',
                      'are', 'our', 'has']

    words = list(dict.keys())
    for word in words:
        if word in commonWordList:
            del(dict[word])
        elif len(word) <= 2:
            del (dict[word])
        elif not word.isalpha():
            del (dict[word])

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
'''

def read_emails_from_directory(directory):
    emailList = []
    for file in os.listdir(directory):
        emailList.append(os.path.join(directory, file))

    listOfWords = []

    for email in emailList:
        current = open(email, encoding='latin-1')
        lines = current.readlines()
        for i in lines:
            word = i.split()
            listOfWords += word

    wordFrequency = collections.Counter(listOfWords)
    wordFrequency = remove_common_words(wordFrequency)

    return wordFrequency.most_common(500)

if __name__ == "__main__":
    print('Enter directory: ')
    directory = input()
    print(read_emails_from_directory(directory))
    # directory input:
    #   C:\Users\Brad\PycharmProjects\EmailReader\spam
    # which I got from;
    #   http://www2.aueb.gr/users/ion/data/enron-spam/

    # Output Example:
    # ... ('these', 330), ('free', 314), ('within', 313), ('pills', 311), ('size', 306) ...




