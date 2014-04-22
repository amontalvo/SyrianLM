'''
Created on Mar 21, 2014

@author: andy
'''

import unittest
from edu.fitchburgstate.taylor.arabic.base.feature import featuretag, readFeatureTag

class featureTest(unittest.TestCase):
    f1text = 'AR(la)'
    f2text = 'AR(la definite=1)'
    f3text = 'NOUN(vasos case=subject gender=masc number=plural)'
    f4text = 'VERB(corremos aspect=imperfect number=plural person=1)'
    f5text = 'VERB(comemos aspect=imperfect number=plural person=1)'
    f6text = 'VERB(como aspect=imperfect number=singular person=1)'
    f7text = 'VERB(comi aspect=perfect number=singular person=1)'

    ft4fullgeneral = ['VERB(aspect=perfect number=singular person=1)',
                      'VERB(aspect=perfect number=singular)',
                      'VERB(number=singular person=1)',
                      'VERB(aspect=perfect person=1)',
                      'VERB(number=singular)',
                      'VERB(aspect=perfect)',
                      'VERB(person=1)',
                      'VERB']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testfeaturetag(self):
        f1 = featuretag('la', 'AR')
        self.assertFeatureEquality(featureTest.f1text, f1)
        f2 = featuretag('la', 'AR')
        f2.add('definite', '1')
        self.assertFeatureEquality(featureTest.f2text, f2)
        self.assertTrue(f1 in f2, '{0} should include {1}'.format(str(f2), str(f1)))
        self.assertFalse(f2 in f1, '{0} should include {1}'.format(str(f1), str(f2)))
        f3 = featuretag('vasos', 'NOUN', 'masc', 'plural')
        f3.add('case', 'subject')
        self.assertFeatureEquality(featureTest.f3text, f3)
        f4 = featuretag('corremos', 'VERB', None, 'plural', '1', 'imperfect')
        self.assertFeatureEquality(featureTest.f4text, f4)
        f5 = featuretag('comemos', 'VERB', None, 'plural', '1', 'imperfect')
        self.assertFeatureEquality(featureTest.f5text, f5)
        f6 = featuretag('como', 'VERB', None, 'singular', '1', 'imperfect')
        self.assertFeatureEquality(featureTest.f6text, f6)
        f7 = featuretag('comi', 'VERB', None, 'singular', '1', 'perfect')
        self.assertFeatureEquality(featureTest.f7text, f7)
        
        self.assertFalse(f1.isValidTag('loredo'), "loredo is an invalid tag")
        self.assertTrue(f1.isValidTag('myst3'), "myst3 is a valid tag")

    def testreadFeatureTag(self):
        self.assertFeatureEquality(featureTest.f1text, readFeatureTag(featureTest.f1text))
        self.assertFeatureEquality(featureTest.f2text, readFeatureTag(featureTest.f2text))
        self.assertFeatureEquality(featureTest.f3text, readFeatureTag(featureTest.f3text))
        self.assertFeatureEquality(featureTest.f4text, readFeatureTag(featureTest.f4text))
        self.assertFeatureEquality(featureTest.f5text, readFeatureTag(featureTest.f5text))
        self.assertFeatureEquality(featureTest.f6text, readFeatureTag(featureTest.f6text))
        self.assertFeatureEquality(featureTest.f7text, readFeatureTag(featureTest.f7text))

    def testWriteRead(self):
        self.readWriteRead(featureTest.f1text)
        self.readWriteRead(featureTest.f2text)
        self.readWriteRead(featureTest.f3text)
        self.readWriteRead(featureTest.f4text)
        self.readWriteRead(featureTest.f5text)
        self.readWriteRead(featureTest.f6text)
        self.readWriteRead(featureTest.f7text)

    def testMax(self):
        #__init__(self, transliteration, POS, gender=None, number=None, person=None, aspect=None):
        f3 = readFeatureTag(featureTest.f3text)
        f4 = readFeatureTag(featureTest.f4text)
        f34 = f3.getMax(f4)
        self.assertEqual(None, f34, 
                         "A max between a noun and a verb should be None not {0}".format(str(f34)))

        f5 = readFeatureTag(featureTest.f5text)
        f45 = f4.getMax(f5)
        f45expected = featuretag(None, 'VERB', None, 'plural', '1', 'imperfect')
        self.assertTrue(f45expected.equals(f45), 
                         "Max 4-5 should be {0} not {1}".format(f45expected, f45))

        f6 = readFeatureTag(featureTest.f6text)
        f46 = f4.getMax(f6)
        f46expected = featuretag(None, 'VERB', None, None, '1', 'imperfect')
        self.assertTrue(f46expected.equals(f46), 
                         "Max 4-6 should be {0} not {1}".format(f46expected, f46))

        f7 = readFeatureTag(featureTest.f7text)
        f47 = f4.getMax(f7)
        f47expected = featuretag(None, 'VERB', None, None, '1')
        self.assertTrue(f47expected.equals(f47), 
                         "Max 4-7 should be {0} not {1}".format(f47expected, f47))

        f67 = f6.getMax(f7)
        f67expected = featuretag(None, 'VERB', None, 'singular', '1')
        self.assertTrue(f67expected.equals(f67), 
                         "Max 6-7 should be {0} not {1}".format(f67expected, f67))

    def testMoreGeneral(self):
        ft = readFeatureTag(featureTest.f7text)
        ftlist = ft.get_more_general_list()
        self.assertTrue(ftlist is not None, "more general f7 1 is None")
        self.assertEqual(1, len(ftlist), "first level more general should be length 1")
        ft0 = ftlist[0]
        self.assertFeatureEquality(featuretag(None, 'VERB', None, 'singular', '1', 'perfect'), ft0)
        ft1list = ft0.get_more_general_list()
        ft1strlist = [str(ft1) for ft1 in ft1list]
        self.assertIn(str(featuretag(None, 'VERB', None, 'singular', '1')), ft1strlist, 
                      "Missing more general featuretag")
        self.assertIn(str(featuretag(None, 'VERB', None, 'singular', None, 'perfect')), ft1strlist, 
                      "Missing more general featuretag")
        self.assertIn(str(featuretag(None, 'VERB', None, None, '1', 'perfect')), ft1strlist, 
                      "Missing more general featuretag")

        ft = readFeatureTag(featureTest.f2text)
        ftlist = ft.get_more_general_list()
        self.assertTrue(ftlist is not None, "more general f7 1 is None")
        self.assertEqual(1, len(ftlist), "first level more general should be length 1")
        ft0 = ftlist[0]
        fttest = featuretag(None, 'AR')
        fttest.add('definite', '1')
        self.assertFeatureEquality(fttest, ft0)
        ft1list = ft0.get_more_general_list()
        self.assertTrue(ft1list is not None, "more general f7 1 is None")
        self.assertEqual(1, len(ft1list), "first level more general should be length 1")
        ft1 = ft1list[0]
        ft1test = featuretag(None, 'AR')
        self.assertFeatureEquality(ft1test, ft1)
        self.assertEqual(0, len(ft1.get_more_general_list()), "Can't get any more general")

    def testFullGeneral(self):
        ft = readFeatureTag(featureTest.f7text)
        ftlist = ft.get_full_general()
        ftset = set()
        for ft in ftlist:
            ftset.add(str(ft))
        ftstrset = set()
        for ftstr in featureTest.ft4fullgeneral:
            ftstrset.add(ftstr)
        diff = ftset.symmetric_difference(ftstrset)
        if len(diff) != 0:
            print("Difference = " +str(list(diff)))
        self.assertEqual(0, len(diff), "Difference should be empty")

    def readWriteRead(self, ftext):
        f = readFeatureTag(ftext)
        f1 = readFeatureTag(str(f))
        self.assertTrue(f.equals(f1), "Read write {0} produced {1}".format(str(f), str(f1)))
        self.assertFeatureEquality(f, f1)

    def assertFeatureEquality(self, f1, f2):
        self.assertEqual(str(f1), str(f2), 
                    "Feature not being created correctly '{0}' != {1}".format(str(f2), str(f1)))

if __name__ == "__main__":
    unittest.main()