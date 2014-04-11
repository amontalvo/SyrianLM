'''
Created on Mar 23, 2014

@author: andy
'''
import unittest
from edu.fitchburgstate.taylor.arabic.base.feature import featuretag
from edu.fitchburgstate.taylor.arabic.base.bigram import bigram, readBigram

class bigramTest(unittest.TestCase):

    b1text = "Noun(perro case=subject gender=masc number=singular)..VERB(corre aspect=imperfect number=singular person=3)"
    b2text = "Noun(perros case=subject gender=masc number=plural)..VERB(corren aspect=imperfect number=plural person=3)"
    b3text = "Noun(pavo case=subject gender=masc number=singular)..VERB(come aspect=imperfect number=singular person=3)"
    b4text = "Noun(pavos case=subject gender=masc number=plural)..VERB(comen aspect=imperfect number=plural person=3)"
    b5text = "Noun(pavo case=subject gender=masc number=singular)..VERB(comio aspect=perfect number=singular person=3)"
    b6text = "Noun(pavos case=subject gender=masc number=plural)..VERB(comieron aspect=perfect number=plural person=3)"
    b7text = "VERB(comio aspect=perfect number=singular person=3)..Noun(carne case=object gender=masc number=singular)"
    b8text = "VERB(comieron aspect=perfect number=plural person=3)..Noun(granos case=object gender=masc number=plural)"
    b9text = "Noun(yo case=subject number=singular)..VERB(comi aspect=perfect number=singular person=1)"
    batext = "Noun(yo case=subject number=singular)..ADVERB(nunca)"

    bmoregeneral = {
        b1text: 
            ["Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular person=3)",
             "Noun(case=subject gender=masc number=singular)..VERB(corre aspect=imperfect number=singular person=3)",
             "Noun(case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular person=3)"],
        'Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular person=3)':
            ['Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular)', 
             'Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect person=3)', 
             'Noun(perro case=subject gender=masc number=singular)..VERB(number=singular person=3)', 
             'Noun(case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular)', 
             'Noun(case=subject gender=masc number=singular)..VERB(aspect=imperfect person=3)', 
             'Noun(case=subject gender=masc number=singular)..VERB(number=singular person=3)'],
        'Noun(case=subject gender=masc number=singular)..VERB(corre aspect=imperfect number=singular person=3)':
            ['Noun(case=subject number=singular)..VERB(corre aspect=imperfect number=singular person=3)',
             'Noun(case=subject number=singular)..VERB(aspect=imperfect number=singular person=3)',
             'Noun(gender=masc number=singular)..VERB(corre aspect=imperfect number=singular person=3)',
             "Noun(gender=masc number=singular)..VERB(aspect=imperfect number=singular person=3)",
             'Noun(case=subject gender=masc)..VERB(corre aspect=imperfect number=singular person=3)', 
             'Noun(case=subject gender=masc)..VERB(aspect=imperfect number=singular person=3)'],
        "Noun(case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular person=3)":
            ['Noun(case=subject gender=masc)..VERB(aspect=imperfect person=3)', 
             'Noun(case=subject gender=masc)..VERB(number=singular person=3)', 
             'Noun(case=subject gender=masc)..VERB(aspect=imperfect number=singular)', 
             'Noun(gender=masc number=singular)..VERB(aspect=imperfect person=3)', 
             'Noun(gender=masc number=singular)..VERB(number=singular person=3)', 
             'Noun(gender=masc number=singular)..VERB(aspect=imperfect number=singular)', 
             'Noun(case=subject number=singular)..VERB(aspect=imperfect person=3)', 
             'Noun(case=subject number=singular)..VERB(number=singular person=3)', 
             'Noun(case=subject number=singular)..VERB(aspect=imperfect number=singular)'],
        'Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular)' :
            ['Noun(case=subject gender=masc number=singular)..VERB(number=singular)', 
             'Noun(case=subject gender=masc number=singular)..VERB(aspect=imperfect)', 
             'Noun(perro case=subject gender=masc number=singular)..VERB(number=singular)', 
             'Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect)']
    }

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testbigram(self):
        self.checkCreate('perro', 'subject', 'masc', 'singular', 'corre', 'imperfect', 'singular', 
                         3, True, bigramTest.b1text)
        self.checkCreate('perros', 'subject', 'masc', 'plural', 'corren', 'imperfect', 'plural', 
                         3, True, bigramTest.b2text)
        self.checkCreate('pavo', 'subject', 'masc', 'singular', 'come', 'imperfect', 'singular', 
                         3, True, bigramTest.b3text)
        self.checkCreate('pavos', 'subject', 'masc', 'plural', 'comen', 'imperfect', 'plural', 
                         3, True, bigramTest.b4text)
        self.checkCreate('pavo', 'subject', 'masc', 'singular', 'comio', 'perfect', 'singular', 
                         3, True, bigramTest.b5text)
        self.checkCreate('pavos', 'subject', 'masc', 'plural', 'comieron', 'perfect', 'plural', 
                         3, True, bigramTest.b6text)
        self.checkCreate('carne', 'object', 'masc', 'singular', 'comio', 'perfect', 'singular', 
                         3, False, bigramTest.b7text)
        self.checkCreate('granos', 'object', 'masc', 'plural', 'comieron', 'perfect', 'plural', 
                         3, False, bigramTest.b8text)
        self.checkCreate('yo', 'subject', None, 'singular', 'comi', 'perfect', 'singular', 
                         1, True, bigramTest.b9text)

    def testReadBigram(self):
        self.assertBigramEquality(self.createBigram('perro', 'subject', 'masc', 'singular', 'corre', 
                                                    'imperfect', 'singular', 3, True),
                                 readBigram(bigramTest.b1text));
        self.assertBigramEquality(self.createBigram('perros', 'subject', 'masc', 'plural', 'corren', 
                                                    'imperfect', 'plural', 3, True),
                                 readBigram(bigramTest.b2text));
        self.assertBigramEquality(self.createBigram('pavo', 'subject', 'masc', 'singular', 'come', 
                                                    'imperfect', 'singular', 3, True),
                                 readBigram(bigramTest.b3text));
        self.assertBigramEquality(self.createBigram('pavos', 'subject', 'masc', 'plural', 'comen', 
                                                    'imperfect', 'plural', 3, True),
                                 readBigram(bigramTest.b4text));
        self.assertBigramEquality(self.createBigram('pavo', 'subject', 'masc', 'singular', 'comio', 
                                                    'perfect', 'singular', 3, True),
                                 readBigram(bigramTest.b5text));
        self.assertBigramEquality(self.createBigram('pavos', 'subject', 'masc', 'plural', 
                                                    'comieron', 'perfect', 'plural', 3, True),
                                 readBigram(bigramTest.b6text));
        self.assertBigramEquality(self.createBigram('carne', 'object', 'masc', 'singular', 'comio', 
                                                    'perfect', 'singular', 3, False),
                                 readBigram(bigramTest.b7text));
        self.assertBigramEquality(self.createBigram('granos', 'object', 'masc', 'plural', 
                                                    'comieron', 'perfect', 'plural', 3, False),
                                 readBigram(bigramTest.b8text));
        self.assertBigramEquality(self.createBigram('yo', 'subject', None, 'singular', 'comi', 
                                                    'perfect', 'singular', 1, True),
                                 readBigram(bigramTest.b9text));

    def testReadWrite(self):
        self.checkReadWrite(bigramTest.b1text)
        self.checkReadWrite(bigramTest.b2text)
        self.checkReadWrite(bigramTest.b3text)
        self.checkReadWrite(bigramTest.b4text)
        self.checkReadWrite(bigramTest.b5text)
        self.checkReadWrite(bigramTest.b6text)
        self.checkReadWrite(bigramTest.b7text)
        self.checkReadWrite(bigramTest.b8text)
        self.checkReadWrite(bigramTest.b9text)
        self.checkReadWrite(bigramTest.batext)

    def testMax(self):
        b3 = readBigram(bigramTest.b3text)
        b4 = readBigram(bigramTest.b4text)
        b34 = b3.getMax(b4)
        b34expected = readBigram("Noun(case=subject gender=masc)..VERB(aspect=imperfect person=3")
        self.assertBigramEquality(b34expected, b34)
        self.assertTrue(b34.isValid(), "b34 is valid")

        b7 = readBigram(bigramTest.b7text)
        b8 = readBigram(bigramTest.b8text)
        b78 = b7.getMax(b8)
        b78expected = readBigram("VERB(aspect=perfect person=3)..Noun(case=object gender=masc")
        self.assertBigramEquality(b78expected, b78)
        self.assertTrue(b78.isValid(), "b78 is valid")

        b38 = b3.getMax(b8)
        self.assertFalse(b38.isValid(), str(b38)+" should be invalid")

        b9 = readBigram(bigramTest.b9text)
        b49 = b4.getMax(b9)
        b49expected = readBigram("Noun(case=subject)..VERB()")
        self.assertBigramEquality(b49expected, b49)
        self.assertTrue(b49.isValid(), "b49 is valid")

        ba = readBigram(bigramTest.batext)
        b9a = b9.getMax(ba)
        b9aexpected = readBigram("Noun(yo case=subject number=singular)..None")
        self.assertBigramEquality(b9aexpected, b9a)
        self.assertFalse(b9a.isValid(), "b9a is not valid")

    def testMoreGeneral(self):
        already_created_set = set()
        self.checkMoreGeneral(bigramTest.b1text, already_created_set)
        b1strList = bigramTest.bmoregeneral[bigramTest.b1text]
        for b1str in b1strList:
            self.checkMoreGeneral(b1str, already_created_set)

        bstr = 'Noun(perro case=subject gender=masc number=singular)..VERB(aspect=imperfect number=singular)'
        self.checkMoreGeneral(bstr, already_created_set)

    def testFullGeneral(self):
        b4 = readBigram(bigramTest.b4text)
        blist = b4.get_full_general()
        self.assertEqual(80, len(blist), 'Full general of b4 should contain 80 bigrams')
        bset = set()
        for bg in blist:
            bset.add(str(bg))
        self.assertEqual(80, len(bset), 'All bigrams must be distinct')
        self.assertIn('Noun..VERB', bset, 'Noun..VERB should be present')

    def checkMoreGeneral(self, bstr, already_created_set):
        #print(bstr)
        bg = readBigram(bstr)
        generalList = bg.get_more_general_list(already_created_set)
        if bstr in bigramTest.bmoregeneral: bstrgeneral = bigramTest.bmoregeneral[bstr]
        else: bstrgeneral = []
        self.checkBigramListEquality(generalList, bstrgeneral)

    def checkBigramListEquality(self, bgList, strList):
        testBgSet = set()
        for bg in bgList:
            testBgSet.add(str(bg))
        testStrSet = set()
        for bgstr in strList:
            testStrSet.add(bgstr)
        diff = testBgSet.symmetric_difference(testStrSet)
        if len(diff) != 0:
            print("Difference = " +str(list(diff)))
        self.assertEquals(0, len(diff), "Difference should be empty")

    def checkReadWrite(self, txt):
        txt2 = str(readBigram(txt))
        self.assertEqual(txt, txt2, 
                         "Bigram {0} not created correctly, should be {1} ".format(txt2, txt))

    def checkCreate(self, noun, case, gender, number, verb, aspect, vnumber, person, nounfirst, txt):
        b = self.createBigram(noun, case, gender, number, verb, aspect, vnumber, person, nounfirst)
        self.assertEqual(txt, str(b), 
                         "Bigram {0} not created correctly, should be {1} ".format(b, txt))

    def createBigram(self, noun, case, gender, number, verb, aspect, vnumber, person, nounfirst):
        n = featuretag(noun, 'Noun', gender, number);
        n.add('case', case)
        v = featuretag(verb, 'VERB', None, vnumber, person, aspect);
        if nounfirst: b = bigram(n, v)
        else: b = bigram(v, n)
        return b

    def assertBigramEquality(self, f1, f2):
        self.assertEqual(str(f1), str(f2), 
                    "Bigram not being created correctly '{0}' != {1}".format(str(f2), str(f1)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()