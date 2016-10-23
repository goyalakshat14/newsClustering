#to parse html
from HTMLParser import HTMLParser
#to parse feed
import feedparser
#stop word corpus
from nltk.corpus import stopwords
#stemming library
from nltk.stem.porter import *
#tokenization library
from nltk import word_tokenize

#tokenize feed function
def feedTokenize(feed):
    newSummary = []
    # extract the summary part of first feed
    for entries in feed.entries:
        summary = entries.summary

        #preprocssing the summary and tokenizing it
        token = word_tokenize(preProcess(summary))
        #print token
        newSummary.append(token)
    
    return newSummary    
#end of feedTokenize

#preProcessing function
def preProcess(summary):
    #remove the html tags from summary
    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    sum = strip_tags(summary)

    #remove unicode letter
    #sum = sum.decode('string_escape')

    #remove stop words
    text = ' '.join([word for word in sum.split() if word not in (stopwords.words('english'))])

    #stemming
    stemmer = PorterStemmer()
    stemmedText = ' '.join([stemmer.stem(word) for word in text.split() ])

    return stemmedText
#end of preProcess

#document vectorizing function
def vectorize(texts):
    # document term frequency
    dtf = []
    #actual vectoriztion
    for text in texts:
        tf = {}
        for token in text:
            if(token in tf):
                tf[token] += 1
            else:
                tf[token] =1
        dtf.append(tf)

    return dtf
#end of vectorize function



######################################################################
######################--program starts here--#########################
######################################################################

#get all the feed from the rss
lifehacker = feedparser.parse("http://www.lifehacker.co.in/rss_section_feeds/18906387.cms")

#tokenize feed
textToken = feedTokenize(lifehacker)

#vectoring the document
documentVec = vectorize(textToken)


