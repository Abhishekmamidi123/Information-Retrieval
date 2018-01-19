# Command line format for running this file:
# python PageRank.py <datafile> <N>
# N - NUmber of pages to be retrieved based on the their pagerank.

# For testing purposes: http://www.cs.princeton.edu/~chazelle/courses/BIB/pagerank.htm
# Damping factor used d = 0.85
# 1-d = 0.15
# Formulae for finding PageRanks
# PR(A) = (1-d) + d*( PR(B)/L(B) + PR(C)/L(C) + ........)
# PR(A) = (1-d) + d*s

# Variables:
# pages: Is a numpy list that stores all the page id's
# pageLinks: Is a dictionary in which 'key' is a pageid and the 'value' is a list contains page id's. ['key'(This page) has outlinks to the pages that are in the 'value' ]

# Tested on the data from http://amitavadas.com/PageRank/sample-large.txt
# Top 10 Retrieved pages are:
# 8669492
# 9369084
# 12486146
# 10912914
# 12787320
# 9265639
# 11775232
# 9520006
# 8614504
# 10936880

import sys
import numpy as np
np.set_printoptions(threshold='nan')
pageLinks = {}
pages = []
sortedPages = []

# Read data from the file and store the pages and their links in their respective list or dictionary.
def preprocessData(filename):
    f = open(filename, 'r')
    for line in f:
        l = line.split()
        pages.append(l[0])
        pageLinks[l[0]] = l[1:]

# find PageRanks of all pages and iterate for some iterations tll it converges.
def findPageRanks(iterations):
    N = len(pages)
    PR_prev = np.ones(N)
    iterations = iterations
    while(iterations>0):
        PR_present = np.zeros(N)
        for i in range(N):
            s = 0
            for j in range(N):
                if j!=i:
                    if pages[i] in pageLinks[pages[j]]:
                        num = PR_prev[j]
                        den = len(pageLinks[pages[j]])
                        s = s + (num/den)
            if s==0:
                s=0
            PR_present[i] = 0.15 + (0.85)*(s)
        PR_prev = PR_present
        iterations = iterations - 1
    # Sort the pages based on the their pageranks
    global sortedPages
    sortedPages = [x for _,x in sorted(zip(PR_present, pages))][::-1]

# Display top N pages baesd on thier page ranks.
def displayTopPages(N):
    print "\nTop " + str(N) + " pages\n"
    if N>len(sortedPages):
    	N = len(sortedPages)
    for i in range(N):
        print sortedPages[i]
    print '\n'

# pagerank_data
filename = sys.argv[1]
iterations = 10
preprocessData(filename)
findPageRanks(iterations)
N = int(sys.argv[2])
displayTopPages(N)
