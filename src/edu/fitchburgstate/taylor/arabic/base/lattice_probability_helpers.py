'''
Created on May 6, 2014

@author: andy
'''
import traceback
from scipy import stats
import math

class LatticeProbabilityHelper:
    '''
    Base class for figuring out the probability of a bigram, given a bigram lattice.
    '''

    def __init__(self, lattice):
        '''
        @param lattice: the bigram lattice that will be used to calculate the probability
        '''
        self.lattice = lattice
        self.probs_done = 0 # keep track of how many probabilities calculated
        self.fallbacks_done = 0 # keep track of how many times we had to fall back to a simpler calculation

    def getProbability(self, item):
        '''
        Calculates the probability of a bigram.

        @param item: bigram
        @return: bigram probability
        '''
        return 0

class SimpleLaplaceCount(LatticeProbabilityHelper):
    '''
    Calculate probability using a simple count base probability ratio, using +1 smoothing.
    '''

    def __init__(self, bigram_lattice):
        '''
        @param lattice: the bigram lattice that will be used to calculate the probability
        '''
        LatticeProbabilityHelper.__init__(self, bigram_lattice)

    def getProbability(self, item):
        '''
        Calculates the probability of a bigram.

        @param item: bigram
        @return: bigram probability
        '''

        self.probs_done += 1
        bigram = self.lattice.getLeast(item)
        if bigram is None:
            return 1.0/self.lattice.getN() # temp hack
        bgcount = self.lattice.getCount(bigram) # count of bigram matching this one
        strtag1 = str(bigram.tag1)
        t2count = self.lattice.unigrams.getCount(bigram.tag2) # count of times tag2 was in corpus
        if strtag1 in self.lattice.tag1_nodes and t2count > 0:
            # Need to take into account that Laplace artificially inflates probabilities
            tag1_nodes = self.lattice.tag1_nodes[strtag1]
            t1nodecount = len(tag1_nodes) # count of distinct node starting with tag1
            denom = t2count + t1nodecount
        else: denom = t2count + 1
        p = (bgcount + 1)/denom
        return p

class GoodTuringEstimators(SimpleLaplaceCount):
    '''
    Good-Turing Estimators using linear regression on (log of r, log of Nr) for estimating 
    expections of Nr. Falls back to a simple count base probability using Laplace smoothing if
    can't calculate line. There are a number of reasons why we may not be able to use Good-Turing
    as I have designed it here. I use a linear regression to calculate the estimated Nr. This
    means that if we have a situation where the slope > -1, or the intercept <= 0, then the Nr
    estimates were not a good candidate. Also, if we have only one point, we can't do a linear
    regression.
    
    Unfortunately, this is a little bit of a pain, because we have to figure out the values for
    p(wn|wn-1). This means that for every wn-1, i.e. tag1 we come across, we will have to do a 
    Good-Turing estimation. Additionally, I'm not certain that Good-Turing works in this case, 
    because of the hierarchical nature of the lattice.
    '''

    NO_EST = (0,0,0,0,0,0,0)

    def __init__(self, bigram_lattice):
        '''
        @param lattice: the bigram lattice that will be used to calcalate the probability
        '''
        SimpleLaplaceCount.__init__(self, bigram_lattice)
        self.linear_parameters = {}

    def getProbability(self, item):
        '''
        returns probability r*/N where
        r* = (r+1)*E(N(r+1))/E(N(r))

        @param item: bigram
        @return: bigram probability
        '''

        least_item = self.lattice.getLeast(item)
        if least_item is None: return 1.0/self.lattice.getN()
        r = self.lattice.getCount(least_item)
        est = self._calculateLinear(least_item)
        prob = self._calculateProb(r, est)
        if prob == 0:
            self.fallbacks_done += 1
            return SimpleLaplaceCount.getProbability(self, least_item)
        else:
            self.probs_done += 1
            return prob

    def _calculateLinear(self, bigram):
        '''
        Calculate the linear regression on the Nr, so that we can calculate expected Nrs
        
        @param bigram: the bigram for which we are calculating the probability
        @return: a tuple containing the linear regression values
        @postcondition: never returns None
        '''

        strtag1 = str(bigram.tag1)
        if strtag1 in self.linear_parameters:
            return self.linear_parameters[strtag1]
        else: 
            Nrs = self._getCounts(bigram)
            N = self.lattice.unigrams.getKeyCount(strtag1)
            X = []
            Y = []
            if len(Nrs) < 2:
                # Can't do linear regression
                print("Can't do linear regression on {0} Nrs count: {1} N:{2}".format(str(bigram), len(Nrs), N))
                est = GoodTuringEstimators.NO_EST
            else:
                # Want to get linear regression on log-log of r to Nr
                maxR = 0
                for r in Nrs:
                    if r > maxR: maxR = r
                    X.append(math.log(r))
                    Y.append(math.log(Nrs[r]))
                try:
                    slope, intercept, r, p, stderr = stats.linregress(X,Y)
                    if slope > -1 or intercept <= 0:
                        #print("Intercept {0} <= 0 for {1}, or slope > -1 for {2}".format(intercept, strtag1, slope))
                        est = GoodTuringEstimators.NO_EST
                    else:
                        forunity = 0;
                        est = (slope, intercept, N, r, p, stderr, 1)
                        # Now normalize
                        for r in range(maxR):
                            p = self._calculateProb(r, est)
                            if p == 0:
                                forunity = 0
                                break;
                            forunity += p
                        if forunity == 0: est = GoodTuringEstimators.NO_EST
                        else: est = (slope, intercept, N, r, p, stderr, 1.0/forunity)
                except:
                    print("Error during linear regression")
                    traceback.print_exc()
                    est = GoodTuringEstimators.NO_EST
            self.linear_parameters[strtag1] = est
            return est

    def _calculateProb(self, r, est):
        '''
        Uses the values from the linear regression to calculate probability
        
        @param r: the number of times the item appeared
        @param est: the tuple calculated in _calculateLinear()
        @return: a non-zero probability if we could use the linear regression values, 0 if not
        '''

        slope = est[0]
        intercept = est[1]
        if slope == 0 and intercept == 0:
            return 0
        else:
            N = est[2]
            # regression is on log, so need to exponentiate
            if r == 0: ENr = intercept
            else: ENr = intercept * math.pow(r, slope) 
            ENr1 = intercept * math.pow(r+1, slope) 
            if ENr1 <= 0 or ENr <= 0: return 0
            else: return est[6]*((r + 1)/N)*(ENr1/ENr)

    def _getCounts(self, bigram):
        '''
        Returns the Nrs for the first item of bigram
        
        @param bigram: the bigram
        @return: hash of r to Nr
        '''

        strtag1 = str(bigram.tag1)
        Nrs = {}
        if strtag1 in self.lattice.tag1_nodes:
            for stritem in self.lattice.tag1_nodes[strtag1]:
                node = self.lattice.findNode(stritem)
                r = node.count
                if r in Nrs:
                    Nrs[r] += 1
                else:
                    Nrs[r]= 1
            # Try at POS level
            if (len(Nrs) < 2):
                least = bigram.getLeast()
                if str(least.tag1) != strtag1:
                    Nrs = self._getCounts(least)
        return Nrs

