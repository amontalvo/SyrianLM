'''
Created on Apr 16, 2014

@author: andy
'''
from .lattice import Lattice
from .bigram import bigram
import math

def simple_laplace_count(n, distinctn, bgcount, t1distinct, t1count, t2distinct, t2count):
    '''
    Calculate probability given the following:
    
    @param  n: the number of bigrams in the reference corpus
    @param distinctn: the number of distinct bigrams in the reference corpus
    @param bgcount: the number of times the bigram appeared in the reference corpus
    @param t1distinct: the number of distinct first tags  in the reference corpus
    @param t1count: the number of times bgcount.tag1 appeared  in the reference corpus as tag1
    @param t2distinct: the number of distinct second tags  in the reference corpus
    @param t2count: the number of times bgcount.tag2 appeared  in the reference corpus as tag2
    '''
    return (bgcount + 1)/(t2count + 1)

class BigramLattice(Lattice):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Prob(of|given)
        Lattice.__init__(self)
        self.tag1s = {}
        self.tag2s = {}

    def addItemAndCount(self, bigram, already_counted = None):
        '''
        Add the item into the lattice if not already present, and increment the ref count
        
        @param ln: an item to add
        @return: the item node
        '''
        self.addBigramCount(bigram, already_counted)
        return Lattice.addItemAndCount(self, bigram, already_counted)

    def addBigramCount(self, bigram, already_counted):
        tag1str = str(bigram.tag1)
        tag1strtag2 = tag1str + "..TAG2"
        tag2str = str(bigram.tag2)
        tag1tag2str = "TAG1.." + tag2str
        if already_counted is None or tag1strtag2 not in already_counted:
            if already_counted is not None: already_counted.add(tag1strtag2)
            if tag1str in self.tag1s:
                self.tag1s[tag1str] += 1
            else:
                self.tag1s[tag1str] = 1
        if already_counted is None or tag1tag2str not in already_counted:
            if already_counted is not None: already_counted.add(tag1tag2str)
            if tag2str in self.tag2s:
                self.tag2s[tag2str] += 1
            else:
                self.tag2s[tag2str] = 1

    def getBigramProbablity(self, trialbigram, probability_func):
        bigram = self.getLeast(trialbigram)
        bgcount = self.getCount(bigram)
        tag1str = str(bigram.tag1)
        if tag1str in self.tag1s:
            t1count = self.tag1s[tag1str]
        else:
            t1count = 0
        t1distinct = len(self.tag1s)
        tag2str = str(bigram.tag2)
        if tag2str in self.tag2s:
            t2count = self.tag1s[tag2str]
        else:
            t2count = 0
        t2distinct = len(self.tag2s)
        n = self.getN()
        distinctCount = self.distinct_itemcount;
        return probability_func(n, distinctCount, bgcount, t1distinct, t1count, t2distinct, t2count)

    def simple_entropy(self, bigramList, probability_func = simple_laplace_count):
        '''
        entry ~= (1/n) log(P(W))
        where W is the corpus
        and P(W) = p(w1 w2 w3 ... wk) ~= p(w1)p(w2|w1)p(w3|w2)...p(wk|w(k-1))
        and p(wi|w(i-1) ~= count(w(i-1)..wi)/count(wi)
        '''
        n = self.getN()
        logprob = math.log2(1/n)
        for bigram in bigramList:
            logprob += math.log2(self.getBigramProbablity(bigram, probability_func))
        return logprob / self.getN()