
# Updated to handle CASIA's lack of name

from subprocess import call
import sys
from os import listdir
from os.path import isfile, join
import csv

lfwDir   = '/home/mbuckler/datasets/lfw/v0/'
casiaDir = '/home/mbuckler/datasets/casia/CASIA-WebFace/'

# Build a dictionary of Casia labels
labels = {}
with open('casia-labels.txt') as csvfile:
  label_file = csv.reader(csvfile, delimiter=' ', quotechar='|')
  for row in label_file:
    labels[row[0]] = row[1]
    
lfwNames     = listdir(lfwDir)
casiaNumbers = listdir(casiaDir)

for number in casiaNumbers:
  if labels[number] in lfwNames:
    print 'Removing '+labels[number]
    call('rm -rf '+casiaDir+number,shell=True)


