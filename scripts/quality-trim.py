#!/usr/bin/env python

import sys
import bz2
import screed
from screed import fastq
import gzip

# python quality-trim.py <input fastq file> <output filtered fastq file>
# MINLENGTH is the minimum lenth of read desired.  NCALLS is the percentage of a read with 'N' base calls for which if read has greater, it will be removed. 

MINLENGTH = 30

if sys.argv[1].endswith('bz2'):
    fp = bz2.BZ2File(sys.argv[1], 'r')
if sys.argv[1].endswith('gz'):
    fp = gzip.open(sys.argv[1], 'r')
if sys.argv[1].endswith('fq'):
    fp = open(sys.argv[1], 'r')

fileout = sys.argv[2]

fw = open(fileout, 'w')

count=0
for n, record in enumerate(fastq.fastq_iter(fp)):
    name = record['name']
    sequence = record['sequence']
    accuracy = record['accuracy']

    sequence = sequence.rstrip('N')
    accuracy = accuracy[:len(sequence)]

    if 'N' in sequence:
       continue
    else:
        trim = accuracy.find('B')

        if trim > MINLENGTH or (trim == -1 and len(sequence) > MINLENGTH):
            if trim == -1:
                fw.write('>%s\n%s\n' % (name, sequence))
            else:
                fw.write('>%s\n%s\n' % (name, sequence[:trim]))
            count += 1

    if n % 1000 == 0:
        print 'scanning', n

print 'Original Number of Reads', n + 1
print 'Final Number of Reads', count
print 'Total Filtered', n + 1  - int(count)
