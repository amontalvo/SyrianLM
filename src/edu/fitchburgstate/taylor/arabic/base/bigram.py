#!/usr/bin/python

from .feature import readFeatureTag

class bigram :
    """
    A bigram is two feature tags, occurring in sequence. Do not change feature tags after bigram
    has been created.
    """
    
    def __init__(self, ft, ft2):
        self.tag1 = ft
        self.tag2 = ft2
        self.strout = None

    # bigram display
    def __str__(self):
        if self.strout is None:
            self.strout = str(self.tag1) + ".." + str(self.tag2)
        return self.strout

    def equals(self, bg):
        return self.tag1.equals(bg.tag1) and self.tag2.equals (bg.tag2)

    def includes(self, bg):
        return self.tag1.includes(bg.tag1) and self.tag2.includes(bg.tag2)

    def getMax(self, bg) :
        """
        return the most-featured bigram which matches both self and bg on non-None features
        """
        return self.leastCommonIncluder(bg)
    
    def isValid(self):
        """
        returns true if neither feature tag is None
        """
        return self.tag1 is not None and self.tag2 is not None

    def leastCommonIncluder(self, bg) :
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
            bg = bigram(ft1, self.tag2)
            strbg = str(bg)
            if already_created_set is None or strbg not in already_created_set:
                if already_created_set is not None: already_created_set.add(strbg)
                returnList.append(bg) 
        for ft2 in tag2_more: 
            bg = bigram(self.tag1, ft2)
            strbg = str(bg)
            if already_created_set is None or strbg not in already_created_set:
                if already_created_set is not None: already_created_set.add(strbg)
                returnList.append(bg) 
            for ft1 in tag1_more: 
                bg = bigram(ft1, ft2)
                strbg = str(bg)
                if already_created_set is None or strbg not in already_created_set:
                    if already_created_set is not None: already_created_set.add(strbg)
                    returnList.append(bg) 
        return returnList

    def get_full_general(self, fulllist = [], already_created_set = set()):
        bglist = self.get_more_general_list(already_created_set)
        fulllist += bglist
        for bg in bglist:
            bg.get_full_general(fulllist, already_created_set)
        return fulllist

class readBigram(bigram):
    """
    A bigram that reads a bigram line
    """

    def __init__(self, line):
        '''
        Read bigram string
        '''
        end1 = line.find('..')
        f1text = line[:end1]
        f2text = line[2 + end1:]
        if f1text == 'None': f1 = None
        else: f1 = readFeatureTag(f1text)
        if f2text == 'None': f2 = None
        else: f2 = readFeatureTag(f2text)
        bigram.__init__(self, f1, f2)
