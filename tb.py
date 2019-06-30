
        
from csv import DictReader
from textblob import TextBlob
class textb(object):
    def __init__(self):
        self.pol=[]
        self.l=0
        self.a1=[]

    def polar_list(self):
        infile='reviews_Data.csv'
        with open(infile,'r') as csvfile:
            #rows=csv.reader(csvfile)
            self.a1=[row["review_text"] for row in DictReader(csvfile)]
            self.l=len(self.a1)
            pol=[]
            for i in range(0,self.l):
                sent=self.a1[i]
                blob=TextBlob(sent)
                #blob.translate(to='en')
                blob.sentiment
                self.pol.append(blob.sentiment.polarity)
        return self.pol
        
    def leng_csv(self):
        return self.l

    def noun_parse(self):

        n=[]
        for i in range(0, self.l):
            sent = self.a1[i]
            blob = TextBlob(sent)
            for np in blob.noun_phrases:
                #print(np)
                n.append(np)
        return n

    def taging(self):
        w=[]
        t=[]
        wt=[]
        for i in range(0, self.l):
            sent = self.a1[i]
            blob = TextBlob(sent)
            for words, tag in blob.tags:
                w.append(words)
                t.append(tag)
        wt=[w,t]
        return wt

