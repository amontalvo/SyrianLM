#!/usr/bin/python

import codecs
from edu.fitchburgstate.taylor.arabic.feature import readFeatureTag
import sys

infile = codecs.open(sys.argv[1])

for line in infile:
	line = line.strip()
	ft = readFeatureTag(line)
	print(ft.__str__())

