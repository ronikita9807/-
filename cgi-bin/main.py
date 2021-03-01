import sys
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist


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


def score(ratio, eps):
    result = 0
    for elem in ratio:
        if abs(elem[1] - elem[2]) < eps:
            result += 1

    return result / len(ratio)


def text_naturalness(text, sample_len, eps):
    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(text)
    fdist = FreqDist(tokens)

    samples = fdist.most_common(sample_len)

    if len(samples) < 2:
        print("err: samples list is empty")
        return

    pivot = samples[0][1]
    ratio = []
    for i in range(0, len(samples)):
        ratio.append([samples[i][0], round(samples[i][1] / pivot, 3), round(1 / (i + 1), 3)])

    # print_results(ratio)

    return score(ratio, eps)


def main(argv):
    if len(argv) == 1:
        sample_len = 50
        eps = 0.1
    elif len(argv) == 2:
        sample_len = argv[1]
    else:
        sample_len = argv[1]
        eps = argv[2]

    test_file = open("../test.txt", "r")
    text = test_file.read()

    print(text_naturalness(text, sample_len, eps))


if __name__ == "__main__":
    main(sys.argv)
