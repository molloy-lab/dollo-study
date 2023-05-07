import pandas
import numpy
import sys

"""
https://stackoverflow.com/questions/556405/what-do-real-user-and-sys-mean-in-the-output-of-time1
Real is wall clock time - time from start to finish of the call. This is all elapsed time including time slices used by other processes and time the process spends blocked (for example if it is waiting for I/O to complete).
User is the amount of CPU time spent in user-mode code (outside the kernel) within the process. This is only actual CPU time used in executing the process. Other processes and time the process spends blocked do not count towards this figure.
Sys is the amount of CPU time spent in the kernel within the process. This means executing CPU time spent in system calls within the kernel, as opposed to library code, which is still running in user-space. Like 'user', this is only CPU time used by the process. See below for a brief description of kernel mode (also known as 'supervisor' mode) and the system call mechanism.
"""


def reformat_timing(data):
    [m, s] = data.split('m')
    m = float(m)
    s = float(s.replace('s', ''))

    totals = m * 60.0 + s
    totalm = totals / 60.0
    totalh = totalm / 60.0

    return [totals, totalm, totalh]


rt_df = pandas.read_csv("all_runtime.csv", keep_default_na=False)
sc_df = pandas.read_csv("all_dollo_score.csv", keep_default_na=False)

rows = []

ntaxs = [10]
nchrs = [500, 1000, 5000, 10000, 50000]
strht = 2000000
srate = 0.000001
repls = [i for i in range(1, 26)]
mthds = ["dollo-cdp-fast", 
         "paup-dollo-fast-hsearch", 
         "paup-dollo-hsearch",
         "paup-dollo-bnb"]

for ntax in ntaxs:
    for nchr in nchrs:
        for repl in repls:
            print("%d %d %s" % (ntax, nchr, repl))

            # Process DOLLO parsimony scores
            scores = []
            for mthd in mthds:
                if mthd == "dollo-cdp-fast":
                    xmthd = mthd
                else:
                    xmthd = mthd + "-first"
                sc_xdf = sc_df[(sc_df["NTAX"] == ntax) &
                               (sc_df["NCHR"] == nchr) &
                               (sc_df["REPL"] == repl) & 
                               (sc_df["MTHD"] == xmthd)]
                if sc_xdf.shape[0] != 1:
                    sys.exit("1 ERROR!")
                scores.append(sc_xdf.DOLLO.values[0])
            scores = numpy.array(scores)
            if scores.min() != scores.max():
                print("Found difference in DOLLO score!")
                print(scores)

            # Only one difference in score found:
            #   10 10000 24
            #   Found difference in DOLLO score!
            #   [12965 12966 12965 12965] 
            #   
            # so dollo-cdp improves upon the fast heuristic search.
            #   Note we can subtract 10000 (because 1 gain/char) to get
            #   [2965 2966 2965 2965]
            #
            # The score found by Dollo-CDP was 3018. This differnce could
            # be due to the 55 characters in state 1 for the outgroup 0. 
            # We aren't sure how such characters are handled by PAUP*.

            # Process runtime
            times = []
            for mthd in mthds:
                rt_xdf = rt_df[(rt_df["NTAX"] == ntax) &
                               (rt_df["NCHR"] == nchr) &
                               (rt_df["REPL"] == repl) & 
                               (rt_df["MTHD"] == mthd)]
                if rt_xdf.shape[0] != 1:
                    sys.exit("2 ERROR!")
            
                data = reformat_timing(rt_xdf.real.values[0])
                times.append(data[0])

            times = numpy.array(times)
            if times.max() > 5:
                print("Found runtime greater than 5 seconds!")
                print(times)
