'''
Created on Apr 21, 2014

Running this with arguments data/padt.ft data/padt-reserve/ALH20010911.0001_story.ft

@author: andy
'''

import sys
import fileinput
import time
import datetime
import math
#import cProfile
#import pstats

from edu.fitchburgstate.taylor.arabic.base.feature import readFeatureTag
from edu.fitchburgstate.taylor.arabic.base.bigram import bigram
from edu.fitchburgstate.taylor.arabic.base.bigram_lattice import BigramLattice

def doReadBigramLattice(filename, bigramLat):
    ft1 = None
    filegen =  fileinput.input(filelist, openhook = fileinput.hook_encoded('utf8'))
    for ln in filegen:
        ft2 = readFeatureTag(ln)
        if ft1 is not None:
            bg = bigram(ft1, ft2)
            bigramLat.addItem(bg)
        ft1 = ft2

def doReadBigramList(filename, bigramList):
    ft1 = None
    filegen =  fileinput.input(filelist, openhook = fileinput.hook_encoded('utf8'))
    for ln in filegen:
        ft2 = readFeatureTag(ln)
        if ft1 is not None:
            bg = bigram(ft1, ft2)
            bigramList.append(bg)
        ft1 = ft2

if __name__ == '__main__':
    starttime = time.time()
    st = datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S')
    print(st)

    bigramLat = BigramLattice()
    filelist = sys.argv[1:]    # list of args except script name

    #profiler = cProfile.Profile()
    #profiler.enable()
    doReadBigramLattice(filelist[0], bigramLat)
    #profiler.disable()
    #ps = pstats.Stats(profiler).sort_stats('tottime')
    #ps.print_stats()

    endtime = time.time();
    elapsetime = endtime - starttime

    bigramList = []
    doReadBigramList(filelist[1], bigramList)
    
    entropy = bigramLat.simple_entropy(bigramList)
    perplexity = math.pow(2, -entropy)

    #print(featureLat)
    #print(bigramLat)

    print("Read file in {0} seconds".format(elapsetime));
    st = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    print("Perplexity = {0}".format(perplexity))
