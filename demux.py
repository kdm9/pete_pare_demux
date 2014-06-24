from collections import Counter
import itertools as itl
import re
import sys
import multiprocessing as mp

regex = re.compile(r"(.+)TGGAATTCTCGGGTGCCAAGGAACTCCAGTCAC(......)ATCTCGTA")

def fq(fhandle):
    for h, s, _, q in zip(fhandle, fhandle, fhandle, fhandle):
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
    pool = mp.Pool()
    ctr = Counter()
    for bcd, read in pool.imap(match_read, fq(ifp), 10000):
        ctr[bcd] += 1
        if bcd == "NOBCD":
            continue
        else:
            try:
                ofp = ofps[bcd]
            except KeyError:
                ofp = open(sys.argv[2] % bcd, "w")
                ofps[bcd] = ofp
            ofp.write("{}{}{}{}".format(*read))
    pool.close()
    pool.join()
    for k, v in ctr.most_common():
        print "{}\t{: 6d}".format(k, v)

