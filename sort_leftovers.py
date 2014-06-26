from __future__ import print_function
from collections import Counter
import itertools as itl
import re
import sys
import multiprocessing as mp
from skbio.core.alignment import StripedSmithWaterman

adapt = StripedSmithWaterman("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACNNNNNNATCTCGTA")

def fq(fhandle):
    for h, s, _, q in itl.izip(fhandle, fhandle, fhandle, fhandle):
        #yield (h.strip(), s.strip(), _.strip(), q.strip())
        yield (h, s, _, q)


def match_read(read):
    aln = adapt(read[1])
    bcd = "NOBCD"
    if aln.target_begin > 10 and aln.target_begin < 30:
        seq = read[1][:aln.target_begin]
        bcd_start = aln.target_begin + 33
        bcd = read[1][bcd_start:bcd_start + 6]
        seq = "{}{}\n".format(bcd, seq)
        qual =  "{}{}\n".format(read[3][bcd_start:bcd_start + 6], read[3][:aln.target_begin])
        read = (read[0], seq, "+\n", qual)
    return (bcd, read)

if __name__ == "__main__":
    ifp = open(sys.argv[1])
    ctr = Counter()
    iii = 0
    for bcd, read in itl.imap(match_read, fq(ifp)):
        if iii % 100 == 0:
            print("Processed {: 7d} reads. Seen {} barcodes".format(
                iii, len(ctr)), end = '\r', file=sys.stderr)
        iii += 1
        ctr[bcd] += 1
        print("{}{}{}{}".format(*read), end='')
    print("Processed {: 7d} reads. Seen {} barcodes".format(iii, len(ctr)),
          file=sys.stderr)
    for k, v in ctr.most_common():
        print("{}\t{: 6d}".format(k, v), file=sys.stderr)
