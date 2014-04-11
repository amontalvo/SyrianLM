#!/usr/bin/python

import re

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

class featuretag:
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
        self.tags = dict()
        self.add(featuretag.TRANSLITERATION, transliteration)
        self.add(featuretag.POS, POS) # DET,PREP,NOUN,VERB...
        self.add('aspect', aspect)    # perfect, imperfect,.  
        self.add('gender', gender)    # masculine, feminine
        self.add('number', number)    # singular, dual, plural
        if person is not None:
            self.add('person', str(person))    # 1, 2, or 3 for 1st, 2nd, or 3rd
        self.strout = None
        
    def __str__(self):
        if self.strout is None:
            self.strout = self.tags[featuretag.POS]
    
            featurestr = ''
            if featuretag.TRANSLITERATION in self.tags:
                featurestr += self.tags[featuretag.TRANSLITERATION] + ' '
            for feature in featuretag.featurenames:  # want features always in same order.
                if feature in (featuretag.POS, featuretag.TRANSLITERATION) : continue
                if not feature in self.tags : continue
                t = self.tags[feature]
                if t != None:
                    featurestr += feature + '=' + t + ' '
    
            if len(featurestr) > 0:
                self.strout += '(' + featurestr[:len(featurestr)-1] + ')'
        
        return self.strout

    def add(self, ft, value):
        """
        add a feature with a value, raises an error if feature is invalid or is already set
        """
        if value is None or len(value) == 0:return
        if not self.isValidTag(ft):
            raise Exception('Tag {0} is not an acceptable feature'.format(ft))
        if ft in self.tags:
            raise Exception('Tag {0}={1} already exists in {2}'.format(ft, value, self.__str__()))
        self.tags[ft] = value
        self.strout = None

    def equals(self, other):
        """
        comparison functions
        return true iff all features identical
        """
        return str(self) == str(other)

    def includes(self, other):
        """
        return true if all features specified in other match corresponding self feature
        """
        for ft in other.tags:
            if (not (ft in self.tags))  or other.tags[ft] != self.tags[ft] :
                return False
        return True

    def get_more_general_list(self, already_created_set = None):
        returnList = []
        if len(self.tags) > 1:
            if featuretag.TRANSLITERATION in self.tags:
                ftmg = self._new_more_general([ft for ft in self.tags.keys() 
                                               if ft != featuretag.TRANSLITERATION])
                ftmgstr = str(ftmg)
                if already_created_set is None or ftmgstr not in already_created_set:
                    if already_created_set is not None: already_created_set.add(ftmgstr)
                    returnList.append(ftmg)
            else:
                for remove_tag in self.tags.keys():
                    if remove_tag == featuretag.POS: continue
                    ftmg = self._new_more_general([ft for ft in self.tags.keys() 
                                                   if ft != remove_tag])
                    ftmgstr = str(ftmg)
                    if already_created_set is None or ftmgstr not in already_created_set:
                        if already_created_set is not None: already_created_set.add(ftmgstr)
                        returnList.append(ftmg)
        return returnList

    def get_full_general(self, fulllist = [], already_created_set = set()):
        featuretaglist = self.get_more_general_list(already_created_set)
        fulllist += featuretaglist
        for ft in featuretaglist:
            ft.get_full_general(fulllist, already_created_set)
        return fulllist

    def getMax(self, other):
        """
        return most-specified featuretag included in both self and other
        """
        if other == None or self.tags[featuretag.POS] != other.tags[featuretag.POS]: return None
        return self._new_more_general([ft for ft in self.tags.keys() 
                                       if ft in other.tags and self.tags[ft] == other.tags[ft]])

    def setFinite(self):
        self.tags['finite'] = 'F'

    def isValidTag(self, tag):
        return tag in featuretag.featuredict

    def _new_more_general(self, tag_list):
        if len(self.tags) <= 1: return None
        ans = featuretag(None, self.tags[featuretag.POS])
        for ft in tag_list:
            if ft == featuretag.POS: continue
            ans.add(ft, self.tags[ft])
        return ans
    

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
