"""
Create nexus file to run parsimony analysis with PAUP*

Based on the following script: 
"""
import argparse
#import os
#import sys


def main(args):
    # Process outgroup taxa
    if len(args.outgroups) == 1:
        tmp = args.outgroups[0]
        oglist = tmp.split(',')
    else:
        oglist = args.outgroups
    ogs = " ".join(oglist)

    # Get number of characters in the input file
    with open(args.input) as fi:
        for line in fi:
            if line.find("nchar=") > -1:
                break
        tmp = line.split("nchar=")[1]
        nchar = tmp.strip().replace(';', '') 

    # Name output files
    if args.parsimony is None:
        method = "parsimony"  # unordered
    else:
        method = args.parsimony

    if args.bband:
        method += "-bnb"
    elif args.fast:
        method += "-fast-hsearch"
    else:
        method += "-hsearch"

    if args.keep is None:
        keep = nchar
    else:
        keep = args.keep
        method += '-' + str(keep)

    nexfile = args.output + 'paup-' + method + ".nex"
    logfile = args.output + 'paup-' + method + ".log"
    output1 = args.output + 'paup-' + method + ".tre"
    output2 = args.output + 'paup-' + method + "-all.trees"

    with open(nexfile, 'w') as fo:
        fo.write("#NEXUS\n")
        fo.write("BEGIN PAUP;\n")
        fo.write("set autoclose=yes warntree=no warnreset=no;\n")
        fo.write("execute " + args.input + ";\n")
        fo.write("outgroup " + ogs + ";\n")

        if args.parsimony == "dollo":
            fo.write("ctype dollo:1-" + nchar + ";\n")
        elif args.parsimony == "camin-sokal":
            fo.write("ctype irrev:1-" + nchar + ";[irrev=Camin-Sokal]\n")

        if int(keep) < int(nchar):
            fo.write("exclude " + str(keep + 1) + "-" + nchar + ";\n")

        if args.bband:
            fo.write("bandb;\n")
        elif args.fast:
            fo.write("hsearch start=stepwise addSeq=random swap=None nreps=10 rseed=55555;\n")
            fo.write("hsearch start=1 swap=TBR nbest=100 rseed=12345;\n")
        else:
            fo.write("hsearch start=stepwise addSeq=random swap=TBR nreps=100 rseed=12345;\n")

        fo.write("rootTrees;\n")
        #fo.write("contree all/strict=yes treefile=" + output1)
        #fo.write(" format=newick;\n")

        fo.write("savetrees File=" + output2)
        fo.write(" root=yes trees=all format=newick;\n")
        fo.write("END;\n")

    #os.system(args.paup + " -n " + nexfile + " &> " + logfile)
    #os.system("rm " + nexfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #parser.add_argument("-e", "--paup", type=str,
    #                    help="Path to PAUP",
    #                    required=True)

    parser.add_argument("-p", "--parsimony", type=str,
                        help="Parsimony method [None, dollo, camin-sokal]")

    parser.add_argument("-b", "--bband", action="store_true",
                        help="Do branch and bound")

    parser.add_argument("-f", "--fast", action="store_true",
                        help="Do fast heuristic search")

    parser.add_argument("-k", "--keep", type=int,
                        help="Number of characters to keep",
                        required=False)

    parser.add_argument("-i", "--input", type=str,
                        help="Input nexus file",
                        required=True)

    parser.add_argument("-g", "--outgroups", type=str, nargs='+',
                        help="Outgroups e.g. "
                             "\'TaxonU TaxonV TaxonW TaxonX TaxonY TaxonZ\'",
                        required=True)

    parser.add_argument("-o", "--output", type=str,
                        help="Output", required=True)

    main(parser.parse_args())

