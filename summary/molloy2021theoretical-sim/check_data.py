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

modls = ["Palaeognathae"]
nchrs = [500, 1000, 5000, 10000, 50000]
repls = [str("Rep%d" % i) for i in range(1, 26)]
mthds = ["paup-dollo-fast-hsearch",
         "dollo-cdp-fast",
         "paup-dollo-hsearch",
         "paup-dollo-bnb"]

for modl in modls:
    for nchr in nchrs:
        for repl in repls:
            print("%s %d %s" % (modl, nchr, repl))

            # Process DOLLO parsimony scores
            scores = []
            for mthd in mthds:
                if mthd == "dollo-cdp-fast":
                    xmthd = mthd
                else:
                    xmthd = mthd + "-first"
                sc_xdf = sc_df[(sc_df["MODL"] == modl) &
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
            #   Palaeognathae 5000 Rep14
            #   Found difference in DOLLO score!
            #   [6226 6223 6223 6223]
            # so dollo-cdp improves upon fast heuristic search.

            # Process runtime
            times = []
            for mthd in mthds:
                rt_xdf = rt_df[(rt_df["MODL"] == modl) &
                               (rt_df["NCHR"] == nchr) &
                               (rt_df["REPL"] == repl) & 
                               (rt_df["MTHD"] == mthd)]
                if rt_xdf.shape[0] != 1:
                    sys.exit("2 ERROR!")
            
                data = reformat_timing(rt_xdf.real.values[0])
                times.append(data[0])

            times = numpy.array(times)
            if times.max() > 3:
                print("Found runtime greater than 3 seconds!")
                print(times)
