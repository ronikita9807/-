from math import sqrt, log10
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class Similarity:
    def __init__(self, text_1, text_2):
        self.text1 = text_1
        self.text2 = text_2

        text1_vec = self.split_text(self.text1)
        text2_vec = self.split_text(self.text2)

        # self.words_plus_tag1 = [morph.parse(word)[0].normal_form + "_" + morph.parse(word)[0].tag.POS for word in text1_vec]
        # self.words_plus_tag2 = [morph.parse(word)[0].normal_form + "_" + morph.parse(word)[0].tag.POS for word in text2_vec]

        self.text1_vec = [morph.parse(word)[0].normal_form for word in text1_vec]
        self.text2_vec = [morph.parse(word)[0].normal_form for word in text2_vec]

        self.set_words = set(self.text1_vec).union(set(self.text2_vec))
        self.vec1, self.vec2 = self.vectorization()


    @staticmethod
    def split_text(text):
        spis = text
        for sep in [
            "-",
            ",",
            ":",
            ";",
            "(",
            ")",
            "?",
            "!",
            "-",
            '"',
            "»",
            "«",
            "—",
            "[",
            "]",
            "}",
            "{",
            ".",
        ]:
            spis = spis.replace(sep, " ")
        spis = spis.split()
        text1_vec = []
        for elem in spis:
            if elem != "":
                text1_vec.append(elem)
        return text1_vec

    def vectorization(self):
        res1 = [0 for _ in range(len(self.set_words))]
        res2 = [0 for _ in range(len(self.set_words))]
        for i, elem in enumerate(self.set_words):
            res1[i] = self.text1_vec.count(elem)
            res2[i] = self.text2_vec.count(elem)
        return res1, res2

    def cos(self, vec1, vec2):
        sum = 0
        sum1 = 0
        sum2 = 0
        for i in range(len(vec2)):
            sum += vec1[i] * vec2[i]
            sum1 += vec1[i] * vec2[i]
            sum2 += vec2[i] * vec2[i]
        return sum / (sqrt(sum1) * sqrt(sum2))

    def get_jaccard_sim(self):
        a = set(self.text1_vec)
        b = set(self.text2_vec)
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def cos_tf(self):
        return self.cos(self.vec1, self.vec2)

    def idf(self, text):
        spis = text
        spis = spis.replace("!", ".")
        spis = spis.replace("\?", ".")
        spis = spis.split(".")

        for i in range(len(spis)):
            for sep in [
                ",",
                ":",
                ";",
                "(",
                ")",
                "?",
                "!",
                "-",
                '"',
                "»",
                "«",
                "—",
                "[",
                "]",
                "}",
                "{",
                ".",
            ]:
                spis[i] = spis[i].replace(sep, " ")
            spis[i] = spis[i].split()

        lenth = len(spis)
        idf = dict()
        for word in self.set_words:
            idf[word] = 0

        for sentens in spis:
            for word in self.set_words:
                if word in sentens:
                    idf[word] += 1

        return idf, lenth

    def cos_tf_idf(self):
        idf1, len1 = self.idf(self.text1)
        idf2, len2 = self.idf(self.text2)
        tf_idf1 = [0.0 for _ in range(len(self.set_words))]
        tf_idf2 = [0.0 for _ in range(len(self.set_words))]

        for i, word in enumerate(self.set_words):
            if idf1[word]:
                tf_idf1[i] = self.vec1[i] * log10(len1 / idf1[word])
            else:
                tf_idf1[i] = self.vec1[i]
            if idf2[word]:
                tf_idf2[i] = self.vec2[i] * log10(len2 / idf2[word])
            else:
                tf_idf2[i] = self.vec2[i]

        return self.cos(tf_idf1, tf_idf2)

    def text_info(self):
        return len(self.text1_vec), len(self.text2_vec), len(set(self.text1_vec) & set(self.text2_vec))


def result(text1, text2):
    a = Similarity(text1, text2)
    len1, len2, inter = a.text_info()
    return a.cos_tf(), a.cos_tf_idf(), a.get_jaccard_sim(), len1, len2, inter


if __name__ == "__main__":
    text1 = "ИИ - наш друг, и он был дружелюбным."
    text2 = "ИИ и люди всегда были дружелюбны."
    a = Similarity(text1, text2)
    print(a.cos_tf())
    print(a.cos_tf_idf())
    print(a.get_jaccard_sim())
    print(a.text_info())
    print(result(text1, text2))


