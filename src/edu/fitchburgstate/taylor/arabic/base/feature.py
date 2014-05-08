#!/usr/bin/python

import re
from .hierarchical import FeatureHierarchicalItem

def feature(strings, *opts):
    """
    the purpose of the feature() function is to
    pick features out of strings, for example to extract one of 'F' or 'M'
    out of the string string '3MS', you could:
       print feature('3MS','F','M')
    Used to extract features from Buckwalter tags
    """
    for feat in opts:
        if strings.find(feat) >= 0 : return feat
    return None

_featurenames = ('aspect', 'case', 'definite', 'finite', 'gender', 'myst1', 'myst2', 
                   'myst3', 'myst4', 'number', 'person', 
                   'POS', 
                   'transliteration')

def _featuredict_generate():
    count = 0
    featuredict = {}
    for f in _featurenames:
        featuredict[f] = count
        count += 1
    return featuredict

class featuretag(FeatureHierarchicalItem):
    """
    The tags associated with a syntactic unit
    """

    # Some constants 
    TRANSLITERATION = 'transliteration'
    POS = 'POS'

    # a list of feature names currently allowed in a specific order 
    featurenames = _featurenames

    # dictionary list of the same allowed feature names, where the value is the index of the feature
    featuredict = _featuredict_generate()

    def __init__(self, transliteration, POS, gender=None, number=None, person=None, aspect=None):
        FeatureHierarchicalItem.__init__(self)
        self.add(featuretag.TRANSLITERATION, transliteration)
        self.add(featuretag.POS, POS) # DET,PREP,NOUN,VERB...
        self.add('aspect', aspect)    # perfect, imperfect,.  
        self.add('gender', gender)    # masculine, feminine
        self.add('number', number)    # singular, dual, plural
        if person is not None:
            self.add('person', str(person))    # 1, 2, or 3 for 1st, 2nd, or 3rd

    def get_more_general_list(self, already_created_set = None):
        '''
        returns a list of featuretags items that are less specific by one feature
        '''
        returnList = []
        if len(self.features) > 1:
            if featuretag.TRANSLITERATION in self.features:
                ftmg = self._new_more_general([ft for ft in self.features.keys() 
                                               if ft != featuretag.TRANSLITERATION])
                self._add_to_list(ftmg, returnList, already_created_set)
            else:
                for remove_tag in self.features.keys():
                    if remove_tag == featuretag.POS: continue
                    ftmg = self._new_more_general([ft for ft in self.features.keys() 
                                                   if ft != remove_tag])
                    self._add_to_list(ftmg, returnList, already_created_set)
        return returnList

    def get_full_general(self, fulllist = [], already_created_set = set()):
        '''
        returns all the item that are less specific 
        '''
        featuretaglist = self.get_more_general_list(already_created_set)
        fulllist += featuretaglist
        for ft in featuretaglist:
            ft.get_full_general(fulllist, already_created_set)
        return fulllist

    def getLeast(self):
        if len(self.features) > 1: return featuretag(None, self.features[featuretag.POS])
        else: return self

    def getMax(self, other):
        """
        return most-specified featuretag included in both self and other
        """
        return self.mostCommonIncluder(other)

    def mostCommonIncluder(self, other):
        """
        return most-specified featuretag included in both self and other
        """
        if other == None or self.features[featuretag.POS] != other.features[featuretag.POS]: return None
        return self._new_more_general([ft for ft in self.features.keys() 
                                       if ft in other.features and self.features[ft] == other.features[ft]])

    def setFinite(self):
        self.features['finite'] = 'F'

    def isValidFeature(self, tag):
        return tag in featuretag.featuredict

    def isValidTag(self, tag):
        return self.isValidFeature(tag)

    def _new_more_general(self, tag_list):
        if len(self.features) <= 1: return None
        ans = featuretag(None, self.features[featuretag.POS])
        for ft in tag_list:
            if ft == featuretag.POS: continue
            ans.add(ft, self.features[ft])
        return ans

    def __str__(self):
        if self.strout is None:
            self.strout = self.features[featuretag.POS]

            featurestr = ''
            if featuretag.TRANSLITERATION in self.features:
                featurestr += self.features[featuretag.TRANSLITERATION] + ' '
            for feature in featuretag.featurenames:  # want features always in same order.
                if feature in (featuretag.POS, featuretag.TRANSLITERATION) : continue
                if not feature in self.features : continue
                t = self.features[feature]
                if t != None:
                    featurestr += feature + '=' + t + ' '

            if len(featurestr) > 0:
                self.strout += '(' + featurestr[:len(featurestr)-1] + ')'

        return self.strout

class readFeatureTag(featuretag):
    """
    A feature tag that reads a feature tag line
    """

    SPLITTER = re.compile("[ ,()]*")

    def __init__(self, line):
        # print ("line = {0}".format(line))
        line = line.strip()
        parenloc = line.find("(")
        if parenloc >= 0:
            featuretag.__init__(self, None, line[:parenloc])
            for part in re.split(readFeatureTag.SPLITTER, line[parenloc+1:]):
                # print ('part = {0}'.format(part))
                if "=" in part:
                    pair = part.split("=")
                    if len(pair) > 2:
                        raise Exception("Problem reading feature '{0}' from line '{1}'".find(part, line))
                    elif len(pair) == 2:
                        self.add(pair[0], pair[1])
                elif len(part) > 0:
                    self.add(featuretag.TRANSLITERATION, part)
        else:
            featuretag.__init__(self, None, line)
