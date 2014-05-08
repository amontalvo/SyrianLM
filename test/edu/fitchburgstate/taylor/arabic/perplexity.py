'''
Created on Apr 21, 2014

Running this with arguments data/padt.ft data/padt-reserve/ALH20010911.0001_story.ft

@author: andy
'''

import sys
import fileinput
import time
import datetime
import codecs
import pickle

#import cProfile
#import pstats

from edu.fitchburgstate.taylor.arabic.base.feature import readFeatureTag
from edu.fitchburgstate.taylor.arabic.base.bigram import bigram
from edu.fitchburgstate.taylor.arabic.base.bigram_lattice import BigramLattice
from edu.fitchburgstate.taylor.arabic.base.lattice_probability_helpers import GoodTuringEstimators
from edu.fitchburgstate.taylor.arabic.base.lattice_probability_helpers import SimpleLaplaceCount

def doReadBigramLattice(filename, bigramLat):
    starttime = time.time()
    ft1 = bigram.BIGRAM_START
    filegen =  fileinput.input(filename, openhook = fileinput.hook_encoded('utf8'))
    for ln in filegen:
        ft2 = readFeatureTag(ln)
        bg = bigram(ft1, ft2)
        bigramLat.addItem(bg)
        ft1 = ft2
    ft2 = bigram.BIGRAM_END
    bg = bigram(ft1, ft2)
    bigramLat.addItem(bg)
    endtime = time.time();
    elapsetime = endtime - starttime
    print("Read {0} file in {1} seconds. {2} items".format(filename, elapsetime, bigramLat.getN()))
    return elapsetime

def doReadBigramList(filename, bigramList):
    starttime = time.time()
    ft1 = bigram.BIGRAM_START
    filegen =  fileinput.input(filename, openhook = fileinput.hook_encoded('utf8'))
    for ln in filegen:
        ft2 = readFeatureTag(ln)
        if ft1 is not None:
            bg = bigram(ft1, ft2)
            bigramList.append(bg)
        ft1 = ft2
    ft2 = bigram.BIGRAM_END
    bg = bigram(ft1, ft2)
    bigramList.append(bg)
    endtime = time.time();
    elapsetime = endtime - starttime
    print("Read {0} file in {1} seconds. {2} items".format(filename, elapsetime, len(bigramList)))
    return elapsetime

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    starttime = time.time()
    st = datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S')
    print(st)

    bigramLat = BigramLattice()
    filelist = sys.argv[1:]    # list of args except script name

    doReadBigramLattice(filelist[0], bigramLat)
    #f = codecs.open('bigramLat', encoding='utf-8', mode='w+')
    #pickle.dump(bigramLat, f)
    #f.close()

    end1time = time.time();
    elapsetime = end1time - starttime
    print("Read {0} file in {1} seconds. {2} items".format(filelist[0], elapsetime, bigramLat.getN()));

    bigramList = []
    doReadBigramList(filelist[1], bigramList)
    end2time = time.time();
    elapse2time = end2time - end1time
    print("Read {0} file in {1} seconds. {2} items".format(filelist[1], elapse2time, len(bigramList)));

    estimator = SimpleLaplaceCount(bigramLat)
    perplexity = bigramLat.perplexity(bigramList, estimator)
    end3time = time.time();
    elapse3time = end3time - end2time
    print("Simple Laplace perplexity calculation took {0} seconds".format(elapse3time));
    print("Perplexity = {0}".format(perplexity))
    print("Probs done {0}, fallbacks {1}".format(estimator.probs_done, estimator.fallbacks_done))

    estimator = GoodTuringEstimators(bigramLat)
    perplexity = bigramLat.perplexity(bigramList, estimator)
    end3time = time.time();
    elapse3time = end3time - end2time
    print("Good-Turing perplexity calculation took {0} seconds".format(elapse3time));
    print("Perplexity = {0}".format(perplexity))
    print("Probs done {0}, fallbacks {1}".format(estimator.probs_done, estimator.fallbacks_done))

    #print(featureLat)
    #print(bigramLat)

