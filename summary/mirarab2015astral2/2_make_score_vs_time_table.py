import pandas
import numpy
import sys

df = pandas.read_csv("data-score-and-timings.csv", keep_default_na=False)

rows = []

ntaxs = [50, 100, 200]
nchrs = [500, 1000, 5000, 10000, 50000]
strht = 2000000
srate = 0.000001
repls = [i for i in range(1, 26)]

sys.stdout.write("\\begin{table}[!h]\n")
sys.stdout.write("\\caption{This table shows a comparison of Dollo-CDP and best trees found by FastH and SlowH. We show the number of replicates for which Dollo-CDP is better (b), worse (w), or the same (s) in terms of Dollo score. We also show the average difference in parsimony scores across these cases. Runtime (in minutes) is averaged across all replicates for Dollo-CDP (m1) and SlowH (m2)}\n")
sys.stdout.write("\\label{tab:results}\n")
sys.stdout.write("\\centering\n")
sys.stdout.write("\\small\n")
sys.stdout.write("\\begin{tabular}{r c c c c c c c}\n")
sys.stdout.write("\\toprule\n")
sys.stdout.write("& & \\multicolumn{2}{c}{\textit{Dollo-CDP vs. FastH}} & & \\multicolumn{3}{c}{\\textit{Dollo-CDP vs. SlowH}} \\\\ \n")
sys.stdout.write("\\cmidrule{3-4}\n")
sys.stdout.write("\\cmidrule{6-8}\n")
sys.stdout.write("\\# of & & \\# of reps & $\\Delta$ score & & \\# of reps & $\\Delta$ score & Runtime (min) \\\\ \n")
sys.stdout.write("characters & & b/w/s score & for b/w/s & & b/w/s score & for b/w/s & m1/m2\\\\ \n")
sys.stdout.write("\\midrule\n")
sys.stdout.write("")

for ntax in ntaxs:
    sys.stdout.write("\\multicolumn{8}{l}{\\textit{%d taxa}} \\\\[0.25em]\n" % ntax)
    for nchr in nchrs:
        sys.stdout.write("%d" % nchr)

        # Compare fast heuristic to Dollo-CDP
        better = []
        worse = []
        same = []
        for repl in repls:
            xdf = df[(df["NTAX"] == ntax) &
                     (df["NCHR"] == nchr) &
                     (df["REPL"] == repl)]

            paupfast = xdf[(xdf["MTHD"] == "paup-dollo-fast-hsearch-first")].DOLLO.values[0]
            dollocdp = xdf[(xdf["MTHD"] == "dollo-cdp-fast")].DOLLO.values[0]

            if dollocdp < paupfast:
                better.append(paupfast - dollocdp)
            elif paupfast < dollocdp:
                worse.append(dollocdp - paupfast)
            else:
                same.append(0)

        numb = len(better)
        numw = len(worse)
        nums = len(same)
        if numw > 0:
            sys.exit("There must be a bug in the code!")

        if numb > 0:
            tmpb = numpy.mean(better)
            tmpb = numpy.round(numpy.round(tmpb, 3), 2)
            avgb = str("%1.2f" % tmpb)
        else:
            avgb = "NA"

        if nums > 0:
            avgs = "0"
        else:
            avgs = "NA"

        sys.stdout.write(" & & %d/%d/%d & %s/NA/%s" % (numb, numw, nums, avgb, avgs))

        # Compare slow heuristic to Dollo-CDP 
        better = []
        worse = []
        same = []
        for repl in repls:
            xdf = df[(df["NTAX"] == ntax) &
                     (df["NCHR"] == nchr) &
                     (df["REPL"] == repl)]

            dollocdp = xdf[(xdf["MTHD"] == "dollo-cdp-fast")].DOLLO.values[0]
            paupslow = xdf[(xdf["MTHD"] == "paup-dollo-hsearch-first")].DOLLO.values[0]

            if dollocdp < paupslow:
                better.append(paupslow - dollocdp)
            elif paupslow < dollocdp:
                worse.append(dollocdp - paupslow)
            else:
                same.append(0)

        numb = len(better)
        numw = len(worse)
        nums = len(same)

        if numb > 0:
            tmpb = numpy.mean(better)
            tmpb = numpy.round(numpy.round(tmpb, 3), 2)
            avgb = str("%1.2f" % tmpb)
        else:
            avgb = "NA"

        if numw > 0:
            tmpw = numpy.mean(worse)
            tmpw = numpy.round(numpy.round(tmpw, 3), 2)
            avgw = str("%1.2f" % tmpw)
        else:
            avgw = "NA"

        if nums > 0:
            avgs = "0"
        else:
            avgs = "NA"

        sys.stdout.write(" & & %d/%d/%d & %s/%s/%s" % (numb, numw, nums, avgb, avgw, avgs))

        # Process runtime
        xdf = df[(df["NTAX"] == ntax) & (df["NCHR"] == nchr)]

        dollocdp = xdf[(xdf["MTHD"] == "dollo-cdp-fast")].SECS.values
        paupslow = xdf[(xdf["MTHD"] == "paup-dollo-hsearch-first")].SECS.values

        dc = numpy.mean(dollocdp) / 60.0
        dc = numpy.round(numpy.round(dc, 3), 2)

        ps = numpy.mean(paupslow) / 60.0
        ps = numpy.round(numpy.round(ps, 3), 2)

        sys.stdout.write(" & %1.2f/%1.2f \\\\\n" % (dc, ps))

sys.stdout.write("\\bottomrule\n")
sys.stdout.write("\\end{tabular}\n")
sys.stdout.write("\\end{table}\n")

"""
\begin{table}[!h]
\caption{This table shows a comparison of Dollo-CDP and best trees found by FastH and SlowH. We show the number of replicates for which Dollo-CDP is better (b), worse (w), or the same (s) in terms of Dollo score. We also show the average difference in parsimony scores across these cases. Runtime (in minutes) is averaged across all replicates for Dollo-CDP (m1) and SlowH (m2)}
\label{tab:results}
\centering
\small
\begin{tabular}{r c c c c c c c}
\toprule
& & \multicolumn{2}{c}{ extit{Dollo-CDP vs. FastH}} & & \multicolumn{3}{c}{\textit{Dollo-CDP vs. SlowH}} \\ 
\cmidrule{3-4}
\cmidrule{6-8}
\# of & & \# of reps & $\Delta$ score & & \# of reps & $\Delta$ score & Runtime (min) \\ 
characters & & b/w/s score & for b/w/s & & b/w/s score & for b/w/s & m1/m2\\ 
\midrule
\multicolumn{8}{l}{\textit{50 taxa}} \\[0.25em]
500 & & 9/0/16 & 1.56/NA/0 & & 0/0/25 & NA/NA/0 & 0.03/0.14 \\
1000 & & 14/0/11 & 2.43/NA/0 & & 0/0/25 & NA/NA/0 & 0.04/0.19 \\
5000 & & 13/0/12 & 6.54/NA/0 & & 0/0/25 & NA/NA/0 & 0.05/0.45 \\
10000 & & 11/0/14 & 16.09/NA/0 & & 0/1/24 & NA/14.00/0 & 0.06/0.67 \\
50000 & & 12/0/13 & 53.58/NA/0 & & 0/0/25 & NA/NA/0 & 0.16/1.90 \\
\multicolumn{8}{l}{\textit{100 taxa}} \\[0.25em]
500 & & 0/0/25 & NA/NA/0 & & 1/0/24 & 1.00/NA/0 & 0.46/0.46 \\
1000 & & 3/0/22 & 1.00/NA/0 & & 1/0/24 & 3.00/NA/0 & 0.38/1.26 \\
5000 & & 25/0/0 & 6.40/NA/NA & & 0/0/25 & NA/NA/0 & 0.16/3.44 \\
10000 & & 23/0/2 & 12.87/NA/0 & & 0/1/24 & NA/7.00/0 & 0.21/5.56 \\
50000 & & 21/0/4 & 42.81/NA/0 & & 0/2/23 & NA/56.00/0 & 0.56/15.58 \\
\multicolumn{8}{l}{\textit{200 taxa}} \\[0.25em]
500 & & 0/0/25 & NA/NA/0 & & 5/1/19 & 1.20/1.00/0 & 2.19/2.20 \\
1000 & & 0/0/25 & NA/NA/0 & & 0/0/25 & NA/NA/0 & 3.04/2.90 \\
5000 & & 19/0/6 & 1.63/NA/0 & & 0/8/17 & NA/3.00/0 & 1.28/39.29 \\
10000 & & 21/0/4 & 3.10/NA/0 & & 0/6/19 & NA/6.00/0 & 1.72/39.37 \\
50000 & & 25/0/0 & 26.68/NA/NA & & 0/8/17 & NA/23.62/0 & 2.42/93.96 \\
\bottomrule
\end{tabular}
\end{table}
"""
