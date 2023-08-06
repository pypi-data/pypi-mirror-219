from spacy import load
nlp = load("tr_core_news_lg")
class stemmer:
    def __init__(self):
        self.verb_suffixes = [
        {"un": ["uz", ""]},
        {"ün": ["üz", ""]},
        {"uyor": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"üyor": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"ıyor": ["ım", "sın", "ız", "sunuz", "lar", ""]},
        {"iyor": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"yor": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"dı": ["m", "n", "k", "nız", "lar", ""]},
        {"di": ["m", "n", "k", "niz", "ler", ""]},
        {"du": ["m", "n", "k", "nuz", "lar", ""]},
        {"dü": ["m", "n", "k", "nüz", "ler", ""]},
        {"tı": ["m", "n", "k", "nız", "lar", ""]},
        {"ti": ["m", "n", "k", "niz", "ler", ""]},
        {"tu": ["m", "n", "k", "nuz", "lar", ""]},
        {"tü": ["m", "n", "k", "nüz", "ler", ""]},
        {"mış": ["ım", "sın", "ız", "sınız", "lar", ""]},
        {"miş": ["im", "sin", "iz", "siniz", "ler", ""]},
        {"muş": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"müş": ["üm", "sün", "üz", "sünnüz", "ler", ""]},
        {"aca": ["k", "ğım", "ksın", "ğız", "ksınız", "klar", ""]},
        {"ece": ["k", "ğim", "ksin", "ğiz", "ksiniz", "kler", ""]},
        {"sa": ["m", "n", "k", "nız", "lar", ""]},
        {"se": ["m", "n", "k", "niz", "ler", ""]},
        {"malı": ["yım", "sın", "yız", "sınız", "lar", ""]},
        {"meli": ["yim", "sin", "yiz", "siniz", "ler", ""]},
        {"sın": ["ız", "lar", ""]},
        {"sin": ["iz", "ler", ""]},
        {"sun": ["uz", "lar", ""]},
        {"sün": ["üz", "ler", ""]},
        {"ın": ["ız", ""]},
        {"in": ["iz", ""]},
        {"ar": ["ım", "sın", "ız", "sınız", "lar", ""]},
        {"er": ["im", "sin", "iz", "siniz", "ler", ""]},
        {"ur": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"ür": ["üm", "sün", "üz", "sünüz", "lür", ""]},
        {"": ["ma", "me", "y", ""]} # Misc
        ]
        self.ekfiil_suffixes = [
        {"dı": ["m", "n", "k", "nız", "lar", ""]},
        {"di": ["m", "n", "k", "niz", "ler", ""]},
        {"du": ["m", "n", "k", "nuz", "lar", ""]},
        {"dü": ["m", "n", "k", "nüz", "ler", ""]},
        {"tı": ["m", "n", "k", "nız", "lar", ""]},
        {"ti": ["m", "n", "k", "niz", "ler", ""]},
        {"tu": ["m", "n", "k", "nuz", "lar", ""]},
        {"tü": ["m", "n", "k", "nüz", "ler", ""]},
        {"mış": ["ım", "sın", "ız", "sınız", "lar", ""]},
        {"miş": ["im", "sin", "iz", "siniz", "ler", ""]},
        {"muş": ["um", "sun", "uz", "sunuz", "lar", ""]},
        {"müş": ["üm", "sün", "üz", "sünnüz", "ler", ""]},
        {"sa": ["m", "n", "k", "nız", "lar", ""]},
        {"se": ["m", "n", "k", "niz", "ler", ""]},
        {"": ["ma", "me", ""]} # Misc
        ]
        self.mutual_suffixes = [".", "b", "c", "d", "ğ", ""]
        self.cleaner = ".,!-()/"
    def clean(self, text):
        for i in self.cleaner:
            text = text.replace(i, "")
        return text
    def VerbStem(self, word, mode="normal"):
        if(mode=="normal"):
            liste = self.verb_suffixes
        elif(mode=='ekfiil'):
            liste = self.ekfiil_suffixes
        for dict in liste:
            for ek, end in zip(dict.keys(), dict.values()):
                for bitis in end:
                    suffix = ek + bitis

                    word = word.removesuffix(suffix)
        return word
    def NounStem(self, word):
        pass
    def stem(self, word):
        word = self.clean(word)
        print(word)
        if(word.count(" ") == 0): # Single word
            for suffix in self.mutual_suffixes:
                word = word.removesuffix(suffix)
            nlpword = nlp(word)
            for token in nlpword:
                if(token.pos_ == "VERB"):
                    new = self.VerbStem(word, "ekfiil")
                    for suffix in self.mutual_suffixes:
                        new = new.removesuffix(suffix)
                    last = self.VerbStem(new) # In Turkish, a word can take two suffixes.
                    for suffix in self.mutual_suffixes:
                        last = last.removesuffix(suffix)
                    return last
                else:
                    return word
        else:
            sentence = word.split()
            newsentence = ""
            for words in sentence:
                for suffix in self.mutual_suffixes:
                    words = words.removesuffix(suffix)
                nlpword = nlp(words)
                for token in nlpword:
                    if(token.pos_ == "VERB"):
                        new = self.VerbStem(words, "ekfiil")
                        for suffix in self.mutual_suffixes:
                            new = new.removesuffix(suffix)
                        print(new)
                        last = self.VerbStem(new)
                        for suffix in self.mutual_suffixes:
                            last = last.removesuffix(suffix)
                        newsentence += " " + last
                    else:
                        newsentence += " " + words
            return newsentence
stemci = stemmer()
myword = stemci.stem("seviyorum, yapmışım, koşarlar, uyuyordu, yemişsin")
print(myword)