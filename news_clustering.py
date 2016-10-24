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
#used for hashing with md5
import hashlib
#printing time
import time
from datetime import datetime
#maths function
import math
#using counter(sub class of dict) 
from collections import Counter

#hashes all the feed
def hashFeed(feed):
    allFeed = {}
    for entries in feed.entries:
        iD = entries.link
        hasx = hashlib.md5(iD)
        allFeed[hasx] = entries
    return allFeed

#end of hashFeed

#tokenize feed function
def feedTokenize(feed):
    newSummary = {}
    # extract the summary part of first feed
    for iD in feed:
        summary = feed[iD].title

        #preprocssing the summary and tokenizing it
        token = word_tokenize(preProcess(summary))
        #print token
        newSummary[iD] = token
    
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
    dtf = {}
    #actual vectoriztion
    for iD in texts:
        tf = {}
        for token in texts[iD]:
            if(token in tf):
                tf[token] += 1
            else:
                tf[token] =1
        dtf[iD] = tf

    return dtf
#end of vectorize function

#cosine similarity function
def cosineSim(iD , iD2):
    sumTerm = 0
    for term in documentVec[iD]:
        if(term in documentVec[iD2]):
            sumTerm += documentVec[iD][term]*documentVec[iD2][term]

    cosSim = sumTerm/(docSqrRootTotal[iD]*docSqrRootTotal[iD2])
    return cosSim
#end of cosine similarity function


#UPGMA function
def upgma(cluster1 , cluster2):
    A = len(cluster1)
    B = len(cluster2)
    sum = 0
    for iD in cluster1:
        for iD2 in cluster2:
            sum += (1-docCosSim[iD][iD2])
    mean = sum/(A*B)
    return mean
#end of epgma function
######################################################################
######################--program starts here--#########################
######################################################################

threshold = 0.55 

#get all the feed from the rss
print "fetching feed"
print time.strftime('%l:%M:%S%p')
dt = datetime.now()
print dt.microsecond
lifehacker = feedparser.parse("http://www.lifehacker.co.in/rss_section_feeds/18906387.cms")
phonearena = feedparser.parse("http://www.phonearena.com/feed")

#hashFeed
print "hashing the feed"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
dt = datetime.now()
print dt.microsecond
feed = hashFeed(lifehacker)
feed.update(hashFeed(phonearena))

#tokenize feed
print "tokenizing the feed"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
dt = datetime.now()
print dt.microsecond
textToken = feedTokenize(feed)


#vectoring the document
print "vectorizing the token"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
dt = datetime.now()
print dt.microsecond
documentVec = vectorize(textToken)


#Calculating total no of terms
print "calcualting total token in documents"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
docSqrRootTotal = {}
for iD in documentVec:
    sqrtotal  = 0
    for term in documentVec[iD]:
        sqrtotal += documentVec[iD][term]*documentVec[iD][term]
    docSqrRootTotal[iD] = math.sqrt(sqrtotal) 


#cosine similarity
print "calculating similarity"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')

docCosSim = {}
for iD in documentVec:
    cosSim = {}
    for iD2 in documentVec:
        if( iD != iD2 ):
           cosSim[iD2] =  cosineSim(iD,iD2)
    docCosSim[iD] = cosSim


#making cluster
clusters = []
print "making cluster"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
for iD in documentVec:
    if( not clusters):
        clusters.append([iD])
    else :
        means = []
        for cluster in clusters:
            means.append(upgma([iD],cluster))
        
        minVal = min(means)
        print minVal
        if(minVal < threshold):
            clusters[means.index(minVal)].append(iD)
        else:
            clusters.append([iD])

print "clustering complete"
print time.strftime('%l:%M:%S%p %Z on %b %d, %Y')
for cluster in clusters:
    print ""
    print "new cluster"
    for iD in  cluster:
        print feed[iD].title