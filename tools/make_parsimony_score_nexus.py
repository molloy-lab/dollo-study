"""
Create nexus file to run parsimony analysis with PAUP*

Based on the following script: 
"""
import argparse
#import os
#import sys


def main(args):
    # Process outgroup taxa
    #if len(args.outgroups) == 1:
    #    tmp = args.outgroups[0]
    #    oglist = tmp.split(',')
    #else:
    #    oglist = args.outgroups
    #ogs = " ".join(oglist)

    # Get number of characters in the input file
    with open(args.input) as fi:
        for line in fi:
            if line.find("nchar=") > -1:
                break
        tmp = line.split("nchar=")[1]
        nchar = tmp.strip().replace(';', '') 

    # Name output files
    if args.parsimony is None:
        method = "parsimony-score"  # unordered
    else:
        method = args.parsimony + "-score"

    if args.keep is None:
        keep = nchar
    else:
        keep = args.keep
        method += '-' + str(keep)

    tmp = args.tree.rsplit('/', 1)[-1]
    treeprefix = tmp.rsplit('.', 1)[0]

    trefile = args.output + "tree-" + treeprefix + ".nex"
    nexfile = args.output + "paup-" + method + "-tree-" + treeprefix + ".nex"
    logfile = args.output + "paup-" + method + "-tree-" + treeprefix + ".log"

    # Write newick string to nexus file
    with open(args.tree, 'r') as fi:
        line = fi.readline()
    with open(trefile, 'w') as fo:
        fo.write("#NEXUS\n")
        fo.write("begin trees;")
        fo.write("tree mytree = [&R] " + line)
        fo.write(";\n")
        fo.write("End;\n")

    # Write PAUP program to nexus file
    with open(nexfile, 'w') as fo:
        fo.write("#NEXUS\n")
        fo.write("BEGIN PAUP;\n")
        fo.write("set autoclose=yes warntree=no warnreset=no;\n")
        fo.write("execute " + args.input + ";\n")
        fo.write("execute " + trefile + ";\n")
        #fo.write("outgroup " + ogs + ";\n")
        #fo.write("rootTrees;\n")
        fo.write("set criterion=parsimony;\n")
        if args.parsimony == "dollo":
            fo.write("ctype dollo:1-" + nchar + ";\n")
        elif args.parsimony == "camin-sokal":
            fo.write("ctype irrev:1-" + nchar + ";[irrev=Camin-Sokal]\n")
        if int(keep) < int(nchar):
            fo.write("exclude " + str(keep + 1) + "-" + nchar + ";\n")
        fo.write("pscores / single=var;\n")
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

    parser.add_argument("-i", "--input", type=str,
                        help="Input nexus file containing character matrix",
                        required=True)

    parser.add_argument("-k", "--keep", type=int,
                        help="Number of characters to keep",
                        required=False)

    parser.add_argument("-t", "--tree", type=str,
                        help="Input nexus file containing tree",
                        required=True)

    #parser.add_argument("-g", "--outgroups", type=str, nargs='+',
    #                    help="Outgroups e.g. "
    #                         "\'TaxonU TaxonV TaxonW TaxonX TaxonY TaxonZ\'",
    #                    required=True)

    parser.add_argument("-o", "--output", type=str,
                        help="Output", required=True)

    main(parser.parse_args())

