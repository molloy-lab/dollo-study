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


cols = ["NTAX", "STRHT", "SRATE", "NCHR", "REPL",
        "MTHD", "DOLLO", "SECS"]

rows = []

ntaxs = [10, 50, 100, 200]
nchrs = [500, 1000, 5000, 10000, 50000]
strht = 2000000
srate = 0.000001
repls = [i for i in range(1, 26)]

mthds = ["paup-dollo-fast-hsearch-first",
         "dollo-cdp-fast",
         "paup-dollo-hsearch-first",
         "paup-dollo-hsearch"]

for ntax in ntaxs:
    for nchr in nchrs:
        for repl in repls:
            for mthd in mthds:
                #print("%d %d %d %s" % (ntax, nchr, repl, mthd))

                # Process DOLLO parsimony scores
                if (mthd != "dollo-cdp-fast") and (mthd.find("first") < 0):
                    xmthd = mthd + "-first"
                else:
                    xmthd = mthd
                    
                sc_xdf = sc_df[(sc_df["NTAX"] == ntax) &
                               (sc_df["NCHR"] == nchr) &
                               (sc_df["REPL"] == repl) & 
                               (sc_df["MTHD"] == xmthd)]
                if sc_xdf.shape[0] != 1:
                    sys.exit("1 ERROR!")

                score = sc_xdf.DOLLO.values[0]

                # Process runtime
                xmthd = mthd.replace("-first", "")
                rt_xdf = rt_df[(rt_df["NTAX"] == ntax) &
                               (rt_df["NCHR"] == nchr) &
                               (rt_df["REPL"] == repl) & 
                               (rt_df["MTHD"] == xmthd)]
                if rt_xdf.shape[0] != 1:
                    sys.exit("2 ERROR!")
            
                data = reformat_timing(rt_xdf.real.values[0])
                secs = data[0]
                if mthd == "paup-dollo-fast-hsearch-first":
                    save = secs
                elif mthd == "dollo-cdp-fast":
                    secs += save

                row = {}
                row["NTAX"] = ntax
                row["STRHT"] = strht
                row["SRATE"] = srate
                row["NCHR"] = nchr
                row["REPL"] = repl
                row["MTHD"] = mthd
                row["DOLLO"] = score
                row["SECS"] = secs
                rows.append(row)

df = pandas.DataFrame(rows, columns=cols)
df.to_csv("data-score-and-timings.csv",
          sep=',', na_rep="NA",header=True, index=False)
