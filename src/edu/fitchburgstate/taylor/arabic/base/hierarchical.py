'''
Created on Apr 17, 2014

@author: andy
'''

class FeatureHierarchicalItem:
    '''
    Abstract class for feature tags and n-grams
    '''

    def __init__(self, item = None):
        '''
        Constructor.
        
        @param item is dict of features
        '''
        self.features = {}
        if item is not None:
            for feature in item:
                itemfeature = item[feature]
                if itemfeature is not None:
                    self.add(feature, item[feature])
        self.strout = None

    def add(self, feature, value):
        """
        adds a feature with a value, raises an error if feature is invalid or is already set
        """
        if value is None or len(str(value)) == 0:return
        if not self.isValidFeature(feature):
            raise Exception('{0} is not an acceptable feature'.format(feature))
        if feature in self.features:
            raise Exception('Feature {0}={1} already exists in {2}'.format(feature, value, self.__str__()))
        self.features[feature] = value
        self.strout = None

    def equals(self, item2):
        '''
        returns true if items are equal
        '''
        #the string value is cached, so equals should be fast
        return str(self) == str(item2)

    def getMax(self, bg):
        """
        Returns the most-specific item which matches both self and item on non-None features
        """
        return self.mostCommonIncluder(bg)
    
    def isValid(self):
        """
        returns false, let subclass decide
        """
        raise("isValid not implemented")

    def isValidFeature(self, feature):
        """
        returns false, let subclass decide
        """
        raise("isValidFeature not implemented")

    def mostCommonIncluder(self, other):
        """
        Returns the most-specific item which matches both self and item on non-None features
        """
        raise("mostCommonIncluder not implemented")

    def get_more_general_list(self, already_created_set = None):
        '''
        returns a list of Hierarchical items that are less specific by one feature
        '''
        raise("get_more_general_list not implemented")

    def get_full_general(self, fulllist = [], already_created_set = set()):
        '''
        returns a list of all possible  Hierarchical items that are less specific
        '''
        bglist = self.get_more_general_list(already_created_set)
        fulllist += bglist
        for bg in bglist:
            bg.get_full_general(fulllist, already_created_set)
        return fulllist

    def _add_to_list(self, item, addList, already_added_set):
        '''
        adds item to addList, but only if it is not already listed in already_added_set
        '''
        stritem = str(item)
        if already_added_set is None or stritem not in already_added_set:
            if already_added_set is not None:
                already_added_set.add(stritem)
            addList.append(item)

    def __contains__(self, other):
        '''
        returns true if other is less specific than self, or everything in other is also in self
        '''
        for feature in other.features:
            if feature not in self.features: return False
            elif other.features[feature] not in self.features[feature]:
                return False
        return True

    def __iter__(self):
        return iter(self.get_more_general_list())

    def __str__(self):
        '''
        returns string representation
        '''
        # if self.strout is not None, return it
        # else get the string representation of this item, cache it in self.strout then return it
        # the string representation must be distinct enough so that two items are equal, if their
        # string representations are equal
        raise("__str__ Not implemented")
