#!/usr/bin/python

from .feature import readFeatureTag
from .hierarchical import FeatureHierarchicalItem

class fakeFeature:
    def __init__(self, st): self.st = st
    def __str__(self): return self.st
    def get_more_general_list(self, already_created_set = None): return [self]
    def getLeast(self): return self

class bigram(FeatureHierarchicalItem):
    """
    A bigram is two feature tags, occurring in sequence. Do not change feature tags after bigram
    has been created.

    This class is a subclass of FeatureHierarchicalItem, but doesn't use many of the super class's
    methods because the more abstract methods are slightly slower to the tweaked methods.
    """

    BIGRAM_START = fakeFeature("START")
    BIGRAM_END = fakeFeature("END")

    def __init__(self, ft, ft2):
        self.tag1 = ft
        self.tag2 = ft2
        self.strout = None
        self.valid = ft is not None and ft2 is not None

    def add(self, feature, value):
        self.isValidFeature(feature)

    def equals(self, bg):
        return self.tag1.equals(bg.tag1) and self.tag2.equals (bg.tag2)

    def includes(self, bg):
        return self.tag1.includes(bg.tag1) and self.tag2.includes(bg.tag2)

    def isEnd(self):
        return self.tag2 == bigram.BIGRAM_END

    def isStart(self):
        return self.tag1 == bigram.BIGRAM_START

    def isValid(self):
        '''
        returns true if neither feature tag is None
        '''
        return self.valid

    def mostCommonIncluder(self, bg) :
        if self.isValid() and bg.isValid():
            return bigram(self.tag1.getMax(bg.tag1), self.tag2.getMax(bg.tag2))
        else:
            return None

    def get_more_general_list(self, already_created_set = None):
        if not self.isValid(): return 

        tag1_more = self.tag1.get_more_general_list()
        tag2_more = self.tag2.get_more_general_list()

        returnList = []
        for ft1 in tag1_more:
            self._add_to_list(bigram(ft1, self.tag2), returnList, already_created_set)
        for ft2 in tag2_more:
            self._add_to_list(bigram(self.tag1, ft2), returnList, already_created_set)
            for ft1 in tag1_more:
                self._add_to_list(bigram(ft1, ft2), returnList, already_created_set)
        return returnList

    def getLeast(self):
        least = bigram(self.tag1.getLeast(), self.tag2.getLeast())
        if str(least) != str(self): return least
        else: return self

    def __str__(self):
        '''
        string bigram
        '''
        if self.strout is None:
            self.strout = str(self.tag1) + ".." + str(self.tag2)
        return self.strout

class readBigram(bigram):
    """
    A bigram that reads a bigram line
    """

    def __init__(self, line):
        '''
        Read bigram string
        '''
        grams = line.split('..')
        f1text = grams[0]
        f2text = grams[1]
        if f1text == 'None': f1 = None
        elif f1text == bigram.BIGRAM_START: f1 = bigram.BIGRAM_START
        else: f1 = readFeatureTag(f1text)
        if f2text == 'None': f2 = None
        elif f2text == bigram.BIGRAM_END: f2 = bigram.BIGRAM_END
        else: f2 = readFeatureTag(f2text)
        bigram.__init__(self, f1, f2)
