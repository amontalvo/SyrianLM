'''
Created on Apr 10, 2014

@author: andy
'''
import sys
import fileinput

from edu.fitchburgstate.taylor.arabic.base.feature import readFeatureTag
from edu.fitchburgstate.taylor.arabic.base.bigram import bigram
from edu.fitchburgstate.taylor.arabic.base.lattice import Lattice

if __name__ == '__main__':
    featureLat = Lattice()
    bigramLat = Lattice()
    filelist = sys.argv[1:]    # list of args except script name
    ft1 = None
    for filename in filelist:
        filegen =  fileinput.input(filelist, openhook = fileinput.hook_encoded('utf8'))
        for ln in filegen:
            ft2 = readFeatureTag(ln)
            featureLat.addItem(ft2)
            if ft1 is not None:
                bg = bigram(ft1, ft2)
                bigramLat.addItem(bg)
            ft1 = ft2
    print(featureLat)
    print(bigramLat)
