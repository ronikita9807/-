import sys
import math
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords


# nltk.download('all')

def print_tokens(tokens):
    for token in tokens:
        print(token)
        print()

    return


def dict_to_list(dict):
    lst = []
    for key, value in dict.iteritems():
        temp = (key, value)
        lst.append(temp)

    return lst


def print_results(ratio):
    print("Word | ratio | standard")
    for elem in ratio:
        print('{} | {} | {}'.format(elem[0], elem[1], elem[2]))

    return


def score(ratio):
    if len(ratio) < 1000:
        eps = 0.1
    elif len(ratio) < 10000:
        eps = 0.01
    else:
        eps = 0.001

    result = 0
    for elem in ratio:
        if abs(elem[1] - elem[2]) < eps:
            result += 1

    return result / len(ratio)


def text_naturalness(text):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(text.lower())

    fdist = FreqDist(tokens)

    samples = fdist.most_common(len(tokens))
    # print(samples)

    if len(samples) < 2:
        print("err: samples list is empty")
        return

    unique = 0
    significant = 0
    sickness = 0
    pivot = samples[0][1]
    ratio = []
    for i in range(0, len(samples)):
        ratio.append([samples[i][0], round(samples[i][1] / pivot, 3), round(1 / (i + 1), 3)])
        if samples[i][1] == 1:
            unique += 1
        if samples[i][1] > len(tokens) * 0.000001:
            significant += 1

    # print_results(ratio)

    stop_words = set(stopwords.words("russian"))
    sw = [token for token in tokens if token in stop_words]

    without_sw = [token for token in tokens if token not in stop_words]
    fd = FreqDist(without_sw)
    top_word = fd.most_common(1)

    return score(ratio), len(tokens), len(sw), unique, significant, round(math.sqrt(top_word[0][1]), 3)


def main(argv):
    test_file = open("../test.txt", "r")
    text = test_file.read()

    print(text_naturalness(text))


if __name__ == "__main__":
    main(sys.argv)
