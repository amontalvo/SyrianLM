'''
Created on Apr 10, 2014

@author: andy
'''
import sys
import fileinput
import time
import datetime
#import cProfile
#import pstats

from edu.fitchburgstate.taylor.arabic.base.feature import readFeatureTag
from edu.fitchburgstate.taylor.arabic.base.bigram import bigram
from edu.fitchburgstate.taylor.arabic.base.lattice import Lattice

def doRead(filename):
    ft1 = None
    filegen =  fileinput.input(filelist, openhook = fileinput.hook_encoded('utf8'))
    for ln in filegen:
        ft2 = readFeatureTag(ln)
        featureLat.addItem(ft2)
        if ft1 is not None:
            bg = bigram(ft1, ft2)
            bigramLat.addItem(bg)
        ft1 = ft2

if __name__ == '__main__':
    starttime = time.time()
    st = datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d %H:%M:%S')
    print(st)

    featureLat = Lattice()
    bigramLat = Lattice()
    filelist = sys.argv[1:]    # list of args except script name

    #profiler = cProfile.Profile()
    #profiler.enable()
    for filename in filelist:
        doRead(filename)
    #profiler.disable()
    #ps = pstats.Stats(profiler).sort_stats('tottime')
    #ps.print_stats()

    endtime = time.time();
    elapsetime = endtime - starttime

    feature_leaf_set = featureLat.getDistinctKeySet();
    num_words = featureLat.getN();
    bigram_leaf_set = bigramLat.getDistinctKeySet();

    #print(featureLat)
    #print(bigramLat)

    print("Read file in {0} seconds".format(elapsetime));
    st = datetime.datetime.fromtimestamp(endtime).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
