'''
Created on Apr 16, 2014

@author: andy
'''
from .lattice import Lattice, LatticeNode
from .bigram import bigram
import math

class BigramLattice(Lattice):
    '''
    Lattice specific to bigram type lattices. That is, two items, where the items are used
    to calculate probabilities. The bigram here does not strictly have to be a word bigram
    but can be an n-gram, followed by a singleton.
    '''

    def __init__(self):
        '''
        Constructor. Keep track of number of tags in first and second position of bigram
        '''
        # Prob(of|given)
        Lattice.__init__(self)
        self.unigrams = Lattice()
        self.tag1_nodes = {}

    def addItem(self, bigram):
        Lattice.addItem(self, bigram)
        tag1 = bigram.tag1
        tag1s = str(tag1)
        if tag1s != bigram.BIGRAM_START and tag1s != bigram.BIGRAM_END:
            self.unigrams.addItem(tag1) 

    def perplexity(self, bigramList, probability_helper):
        '''
        returns the perplexity 

        @param bigramList: as list of bigrams that will be used to calculate the entropy of the
                model
        @param probability_helper: the object to be used to calculate the probability of individual
                bigrams

        @return: perplexity
        @see: lattice_probability_helpers
        '''
        return math.pow(2, -self.simpleEntropy(bigramList, probability_helper))

    def simpleAddItem(self,item):
        '''
        Add the item into the lattice if not already present, does not increment ref count
        
        @param item: an item with str
        @return node: new or found node
        '''
        if str(item) in self.nodes: return self.nodes[str(item)]
        else:
            node = self.addNode(LatticeNode(item))
            strtag1 = str(item.tag1)
            if strtag1 not in self.tag1_nodes:
                self.tag1_nodes[strtag1] = set()
            self.tag1_nodes[strtag1].add(str(node.item))
            return node

    def simpleEntropy(self, bigramList, probability_helper):
        '''
        returns entropy given a bigram list from another corpus, and a probability helper
        
        entry ~= (1/n) log(P(W))
        where W is the corpus
        and P(W) = p(w1 w2 w3 ... wk) ~= p(w1)p(w2|w1)p(w3|w2)...p(wk|w(k-1))
        and p(wi|w(i-1) ~= count(w(i-1)..wi)/count(wi)
        
        @param bigramList: as list of bigrams that will be used to calculate the entropy of the
                model
        @param probability_helper: the object to be used to calculate the probability of individual
                bigrams. 

        @return: entropy
        @see: lattice_probability_helpers
        '''
        logprob = 0
        count = 0
        for bigram in bigramList:
            count += 1
            if count % 1000 == 0:
                print("Processed {0} items".format(count))
            p = probability_helper.getProbability(bigram)
            try: 
                logprob += p*math.log2(p)
            except:
                print("Could not log "+str(p))
        return logprob #/ self.getN()
