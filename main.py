import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords

#nltk.download('all')

def main():
    test_file = open("test.txt", "r")
    text = test_file.read()

    tokenizer = RegexpTokenizer(r'\w+')

    tokens = tokenizer.tokenize(text)
    for token in tokens:
        print(token)
        print()

if __name__ == "__main__":
    main()