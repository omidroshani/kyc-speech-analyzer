import random

class TextGenerator:

    def __init__(self):
        self.vocabs = open('vocabs.csv','r', encoding="utf-8").readlines()
        self.sentences = open('sentences.csv','r', encoding="utf-8").readlines()

    def random_vocab(self,count = 3):
        data = []
        for i in range(count):
            index = random.randint(0,len(self.vocabs))
            data.append(self.vocabs[index].replace('\n',''))
        return data

    def random_sentence(self,count = 1):
        data = []
        for i in range(count):
            index = random.randint(0,len(self.sentences))
            data.append(self.sentences[index].replace('\n',''))
        return data
