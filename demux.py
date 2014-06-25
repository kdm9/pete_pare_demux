from __future__ import print_function
from collections import Counter
import itertools as itl
import re
import sys
import multiprocessing as mp

regex = re.compile(r"(.+)TGGAATTCTCGGGTGCCAAGGAACTCCAGTCAC(ATCACG|CGATGT|TTAGGC|TGACCA|ACAGTG|GCCAAT|CAGATC|ACTTGA|GATCAG)ATCTCGTA")

def fq(fhandle):
    for h, s, _, q in itl.izip(fhandle, fhandle, fhandle, fhandle):
        #yield (h.strip(), s.strip(), _.strip(), q.strip())
        yield (h, s, _, q)


def match_read(read):
    match = regex.search(read[1])
    if match is None:
        seq = read[1]
        bcd = "NOBCD"
    else:
        seq = match.groups()[0] + "\n"
        bcd = match.groups()[1]
    return (bcd, (read[0], seq, "+\n", read[3]))

if __name__ == "__main__":
    ifp = open(sys.argv[1])
    ofps = {}
    ctr = Counter()
    iii = 0
    #pool = mp.Pool()
    #for bcd, read in pool.imap(match_read, fq(ifp), 10000):
    for bcd, read in itl.imap(match_read, fq(ifp)):
        if iii % 10000 == 0:
            print("Processed {: 7d} reads. Seen {} barcodes".format(
                iii, len(ctr)), end = '\r')
        iii += 1
        ctr[bcd] += 1
        try:
            ofp = ofps[bcd]
        except KeyError:
            ofp = open(sys.argv[2] % bcd, "w")
            ofps[bcd] = ofp
        ofp.write("{}{}{}{}".format(*read))
    print("Processed {: 7d} reads. Seen {} barcodes".format(iii, len(ctr)))
    #pool.close()
    #pool.join()
    for k, v in ctr.most_common():
        print("{}\t{: 6d}".format(k, v))
