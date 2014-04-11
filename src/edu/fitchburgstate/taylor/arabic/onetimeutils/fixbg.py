#!/usr/bin/python

from edu.fitchburgstate.taylor.arabic.base.feature import readFeatureTag
from edu.fitchburgstate.taylor.arabic.base.bigram import readBigram
import codecs
import re

# this file reads the backup.bg file and writes the padt.bg file
# it is a one-time use program to make sure that all the featuretags are in
# the same order,so that we can use the string as a key.
# 

CommentLine = re.compile (r"^#.*")
Nline = re.compile(r"^tokens\s*=\s*(\d+)")
Uline = re.compile(r"^([^)]*[)])\s*(\d+)")
Bline = re.compile(r"^([^)]*[)][.][.][^)]*[)])\s*(\d+)$")

infile = codecs.open("backup.bg", "r" , "utf8")
output = codecs.open("padt.bg", 'w', 'utf8')

for line in infile:
    line = line.strip()
    m = CommentLine.match(line)
    if m : 
        output.write(line)
        output.write("\n")
        continue
    m = Nline.match(line)
    if m : 
        output.write(line)
        output.write("\n")
        continue
    m = Uline.match(line)
    if m :
        c = m.group(2)
        u = readFeatureTag(line)
        output.write(u.__str__());
        output.write(' ')
        output.write(c)
        output.write("\n")
        continue
    m = Bline.match(line)
    if m :
        c = m.group(2)
        u = readBigram(line)
        output.write(u.__str__());
        output.write(' ')
        output.write(c)
        output.write("\n")
        continue
 
output.close()
