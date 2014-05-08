#!/usr/bin/python

class LatticeNode:
    """
    the LatticeNode object holds a number of items useful for various
    smoothing algorithms.  For example the number of items in the 
    self.down  dictionary might be the number of unique ways this item can 
    occur, although the Counter structure has a count which tells how
    many level zero items map to it, and that is probably more interesting.
    The Lattice itself I think I'll want for partial matches,
    and the navigation through the lattice is done with the up and down
    pointers in the LatticeNode.  
    The pointers are string keys, which can be used to reconstruct the
    feature item, or to find LatticeNodes in the Lattice, or counts in the
    Counter
    """
    def __init__(self, it):
        self.up = dict()  # holds string keys and integer counts
        self.down = dict() # more keys and counts
        self.key = str(it)
        self.item = it
        self.count = 0
        self.level = 0

    def addUp(self, node):
        if node.key not in self.up:
            self.up[node.key] = node

    def addDown(self, node):
        if node.level >= self.level: self.level = node.level + 1
        if node.key not in self.down:
            self.down[node.key] = node

    def getKey(self): return self.key

    def addRef(self, already_added = None):
        if already_added is None or self.key not in already_added: 
            self.count += 1
            if already_added is not None: already_added.add(self.key)
            for node in self.up.values():
                node.addRef(already_added)

    def get_more_general_list(self, already_created_set = None):
        if len(self.up) > 0:
            nodes = self.up.values()
            already_created_set.addAll([node.key() for node in nodes])
            return list(nodes)
        else:
            return self.item.get_more_general_list(already_created_set)

    def get_full_general(self, fulllist = [], already_added_set = set()):
        return self._get_all_ups(fulllist, already_added_set)

    def str_branch(self, already_str):
        if self.key in already_str: return ""
        already_str.add(self.key)
        s = str(self) + "\n"
        if len(self.down) > 0:
            downlist = sorted(list(self.down.keys()))
            for itemstr in downlist:
                s += self.down[itemstr].str_branch(already_str)
        return s

    def _get_all_ups(self, fulllist, already_added_set):
        for node in self.up.values():
            if node.key not in already_added_set.add(node.key):
                already_added_set.add(node.key)
                fulllist.append(node)
                node._get_all_ups(fulllist, already_added_set)

    def __str__(self):
        s =  str(self.item)+" count:"+str(self.count)+" level:"+str(self.level)
        if len(self.up) > 0:
            s += " up:{"
            ups = []
            for up in self.up:
                ups.append(str(up))
            s += " ".join(sorted(ups))
            s += "}"
        if len(self.down) > 0:
            s += " down:{"
            downs = []
            for down in self.down:
                downs.append(str(down))
            s += " ".join(sorted(downs))
            s += "}"
            
        return s

class Lattice:
    def __init__(self):
        self.nodes = dict()
        self.root_nodes = set()
        self.leaf_keys = set()
        self.itemcount = 0
        self.distinct_itemcount = 0

    def addItem(self, item):
        '''
        Given an item, populate the lattice with the item and its more general generations
        '''
        if str(item) not in self.nodes: self.distinct_itemcount += 1
        self.itemcount += 1
        self._populateParents(item, set())
        self.leaf_keys.add(str(item))

    def simpleAddItem(self,item):
        '''
        Add the item into the lattice if not already present, does not increment ref count
        
        @param item: an item with str
        @return node: new or found node
        '''
        if str(item) in self.nodes: return self.nodes[str(item)]
        else: return self.addNode(LatticeNode(item))

    def addNode(self,node):
        '''
        Add the node into the lattice if not already present, does not increment the ref count
        
        @param node: a LatticeNode
        @return: an item node, may not be the node passed 
        '''
        if node.getKey() in self.nodes:
            return self.nodes[node.getKey()]
        else:
            self.nodes[node.getKey()] = node
            return node

    def addItemAndCount(self, item, already_counted = None):
        '''
        Add the item into the lattice if not already present, and increment the ref count
        
        @param ln: an item to add
        @return: the item node
        '''
        node = self.simpleAddItem(item)
        node.addRef(already_counted)
        return node

    def addItemRelation(self, upper, lower):
        '''
        Adds the nodes to the up and down of the nodes
        
        @param upper: upper will be added to lower.up
        @param lower: lower will be added to upper.down
        '''
        if isinstance(upper, LatticeNode): upperNode = upper
        else: upperNode = self.simpleAddItem(upper)
        if isinstance(lower, LatticeNode): lowerNode = lower
        else: lowerNode = self.simpleAddItem(lower)
        upperNode.addDown(lowerNode)
        lowerNode.addUp(upperNode)

    def getDistinctKeySet(self):
        return set(self.leaf_keys);

    def getN(self):
        return self.itemcount;

    def findItem(self, key):
        '''
        Find the item which matches the key
        
        @param key: the item key
        @return: the item or None if not found
        '''
        if key in self.nodes: return self.nodes[key].item
        else: return None

    def findNode(self, item):
        '''
        Find the node which matches the item
        
        @param key: the item were trying to match
        @return: the item node or None if not found
        '''
        key = str(item)
        if key in self.nodes: return self.nodes[key]
        else: return None

    def getCount(self, item):
        '''
        Find the count for the item which matches the item
        
        @param item: the item were trying to match
        @return: the item count
        '''
        return self.getKeyCount(str(item))

    def getKeyCount(self, key):
        '''
        Find the count for the item whose key matches key 
        
        @param item: the key of the item
        @return: the item count
        '''
        if key in self.nodes: return self.nodes[key].count
        else: return 0

    def getLeast(self, item):
        '''
        Not sure if this is doing what it is suppose to do.
        
        here is the previous documentation
        getLeastIncluder searches the lattice for a node which includes
        the argument.  'inclusion' is the lattice relation.  High, or 'parent'
        nodes include low, or 'child' nodes.  Since it *is* a lattice, not
        every high node includes every low node: 
            parent and child nodes were inserted as the lattice was built.
        ancestor nodes can be computed from parent and child links,
        but there may be a set of ancestors with no relations between them;
        in the case of unigram feature structures, the highest ancestors 
        would be the N parts of speech.
        in the case of bigrams, the highest ancestors would be the N^2
        part of speech bigrams.
        the Counter class has a levels array but not all the ancestors can
        be found at the highest level.  
        I believe from watching the 'noisy' output that the lattice isn't 
        very deep, so it may be quite broad.  
        I've added an ancestors set to the Lattice, so that the search may
        start from there.  
        a different algorithm might index on the first term of a bigram, but
        here I don't know if this Lattice contains unigrams or bigrams
        '''
        key = str(item)
        # if item itself in lattice, return it
        if key in self.nodes: return self.nodes[key].item

        # breadth first
        already_checked = set()
        checklist = item.get_more_general_list(already_checked)
        while len(checklist) != 0:
            matched = {}
            for genItem in checklist:
                genkey = str(genItem)
                if genkey in self.nodes:
                    matched[genkey] = self.nodes[genkey]
            newchecklist = []
            if len(matched) == 0:
                for genItem in checklist:
                    newchecklist += genItem.get_more_general_list(already_checked)
            checklist = newchecklist

        if len(matched) == 0:
            return None

        highestcountitems = []
        highestcount = 0
        lowestlevel = -1
        returnitem = None
        for node in matched.values():
            if lowestlevel == -1 or node.level < lowestlevel:
                lowestlevel = node.level
                highestcount = node.count
                highestcountitems = [node]
                returnitem = node.item
            elif lowestlevel == node.level:
                if node.count > highestcount:
                    returnitem = node.item
                    highestcount = node.count
                    highestcountitems = [node]
                elif node.count == highestcount:
                    highestcountitems.append(node)

        if len(highestcountitems) > 1: 
            print("Chose randomly from {0} items matched".format(len(highestcountitems)))
            for node in highestcountitems:
                print("  "+str(node))
        if returnitem is None:
            returnitem = item.getLeast()
        return returnitem

    def _populateParents(self, item, already_added):
        '''
        Populate the lattice with the items parents
        '''
        stritem = str(item)
        if stritem in already_added:
            self.nodes[stritem].addRef(already_added)
        else:
            node = self.addItemAndCount(item, already_added)
            for upper in item.get_more_general_list():
                self.addItemRelation(upper, node)
                self._populateParents(upper, already_added)
            if len(node.up) == 0: self.root_nodes.add(node)

    def __str__(self):
        s = "item count: "+str(self.itemcount)+" distinct items:"+str(self.distinct_itemcount)+" node count:"+str(len(self.nodes))+"\n"
        s += "roots:\n"
        rootlist = sorted(list(self.root_nodes), key=lambda x: str(x))
        already_str = set()
        for root in rootlist:
            s += "  " +str(root) + "\n"
        for root in rootlist:
            s += root.str_branch(already_str)
        return s

