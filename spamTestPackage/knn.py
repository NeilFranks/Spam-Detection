import csv
import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.model_selection import train_test_split, cross_validate


from spamTestPackage.EmailReader import get_result


def k_nearest_neighbor():

    # df = pd.read_csv('')
    # ham = 0 and spam = 1
    df = pd.read_csv('data.csv', encoding='latin-1', names=['body_word', 'bw_freq', 'subject_words', 'sw_freq', 'body_phrases', 'bp_freq', 'subject_phrases', 'sp_freq', 'class'])
    print(df)
    x = np.array(df.drop(['class'], 1))
    print(df)
    y = np.array(df['class'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    clf = neighbors.KNeighborsClassifier()
    clf.fit(x_train, y_train)
    accuracy = clf.score(x_test, y_test)
    print("accuracy")
    print(accuracy)

# def k_nearest_neighbor(result, p, k):
#
#     distance = []
#     euclidean_distance = 0
#     for section in result:
#         for group in section:
#             for feature in group:
#                 for s in p:
#                     for g in s:
#                         for f in g:
#                             euclidean_distance += math.sqrt((feature[1] - f[1]) ** 2)
#
#                 # euclidean_distance += math.sqrt((feature[1]-feat[0])**2 + (feature[1]-feat[1])**2)
#             distance.append((euclidean_distance, group))
#     distance = sorted(distance)[:k]
#
#     # ham
#     freq1 = 0
#     # spam
#     freq2 = 0
#
#     for d in distance:
#         if d[1] == 0:
#             freq1 += 1
#         elif d[1] == 1:
#             freq2 += 1
#
#     return 0 if freq1 > freq2 else 1
#
# def save_as_text(result):
#     text_file = open("output.txt", "w")
#     for i in result[0]:
#         text_file.write("(" + i[0] + ",")
#         text_file.write(i[1].__str__() + ") ")
#     for i in result[1]:
#         text_file.write("(" + i[0] + ",")
#         text_file.write(i[1].__str__() + ") ")
#     for i in result[2]:
#         text_file.write("(" + i[0] + ",")
#         text_file.write(i[1].__str__() + ") ")
#     for i in result[3]:
#         text_file.write("(" + i[0] + ",")
#         text_file.write(i[1].__str__() + ") ")
#     text_file.close()


if __name__ == '__main__':
    # ham = 0 and spam = 1
    print("HAM")
    ham = get_result()
    print("SPAM")
    spam = get_result()
    with open('data.csv', 'w', newline='', encoding='latin-1') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, len(ham[0])):
            writer.writerow([ham[0][i][0]] + [','] + [ham[0][i][1]] + [','] + [ham[1][i][0]] + [','] +
                                [ham[1][i][1]] + [','] + [ham[2][i][0]] + [','] + [ham[2][i][1]] + [','] +
                                [ham[3][i][0]] + [','] + [ham[3][i][1]] + [','] + ['0'])
        for i in range(0, len(spam[0])):
            writer.writerow([spam[0][i][0]] + [','] + [spam[0][i][1]] + [','] + [spam[1][i][0]] + [','] +
                            [spam[1][i][1]] + [','] + [spam[2][i][0]] + [','] + [spam[2][i][1]] + [','] +
                            [spam[3][i][0]] + [','] + [spam[3][i][1]] + [','] + ['1'])

    k_nearest_neighbor()
