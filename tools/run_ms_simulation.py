"""
Create 
"""
import argparse
import treeswift
import os
import sys

def check_ultrametric(tree):
    epsilon = 1e-6

    tax2len = {}
    for leaf in tree.traverse_leaves():
        tax = leaf.label
        elen = leaf.get_edge_length()
        tax2len[tax] = elen

        # Add branch lengths up to root
        parent = leaf.get_parent()
        while parent.is_root() is False:
            tax2len[tax] += parent.get_edge_length()
            parent = parent.get_parent()

    vals = [val for val in tax2len.values()]
    head = vals[0]

    for val in vals:
        if abs(val - head) > epsilon:
            return 0

    return 1

def main(args):
    # Read tree
    with open(args.input, 'r') as fi:
    	line = fi.readline()
    tree = treeswift.read_tree(line, schema='newick')

    # Check that tree is ultrametric
    if not check_ultrametric(tree):
        sys.exit("Tree is not ultrametric!")
    
    # Create taxon map
    taxa = [l.label for l in tree.traverse_leaves()]
    tax2ind = {}
    for i, x in enumerate(taxa):
        tax2ind[x] = str(i + 1)
    ntax = len(taxa)

    mu = 0.0000000125
    theta = 4 * mu * args.popsize * args.nsites

    # Write ms command to bash file
    bashfile = args.output + "runms.sh"
    msoutput = args.output + "msoutput.txt"
    nexsfile = args.output + "mschars.nex"

    with open(bashfile, 'w') as fo:
        fo.write("#!\\bin\\bash\n")
        fo.write('\n')
        fo.write("%s %d %d \\\n" % (args.ms, ntax, args.nloci))
        fo.write("    -t %1.6f \\\n" % theta)
        fo.write("    -I " + str(ntax) + ' ' + ' '.join(['1'] * ntax) + " \\\n")

        # Do lineage merging based on tree
        for node in tree.traverse_postorder():
            if node.is_leaf():
                tmp = node.label
                node.label = tax2ind[tmp]
                node.pfl = 0.0  # path from leaf
            else:
                [left, right] = node.child_nodes()
                node.label = left.label
                node.pfl = left.pfl + left.get_edge_length()
                cu_halved = node.pfl / (4.0 * args.popsize)

                fo.write("    -ej %1.6f %s %s \\\n" % (cu_halved, right.label, node.label))

        fo.write("    -T \\\n")  # Save locus (gene) trees
        fo.write("    -s %d &> %s\n" % (args.nsites, msoutput))

    # Run ms
    os.system("bash " + bashfile)

    # Read output from ms and store sequence data
    seqs = {}
    for tax in tax2ind.keys():
        seqs[tax] = []

    npatterns = 0
    with open(msoutput, 'r') as fi:
        for line in fi:
            if line.find("positions:") > -1:
                print(line)
                pattern = []
                nzeros = 0
                nones = 0

                for ind in range(0, ntax):
                    line = fi.readline().strip()
                    if line == '0':
                        nones += 1
                    else:
                        nzeros += 1
                    pattern.append(line)

                if (nzeros > 1) and (nones > 1):
                    npatterns += 1
                    for ind in range(0, ntax):
                        tax = taxa[ind]
                        seqs[tax].append(pattern[ind])
                    if npatterns == args.keep:
                        break

    if npatterns != args.keep:
        sys.stdout.write("Did not generate %d parsimony informative sites!\n" % args.keep)

    # Write sequences to nexus file    
    with open(nexsfile, 'w') as fo:
        fo.write("#NEXUS\n\n")
        fo.write("Begin data;\n")
        fo.write("  Dimensions ntax=%d nchar=%d;\n" % (ntax, npatterns))
        fo.write("  Format datatype=standard gap=-;\n")
        fo.write("  Matrix\n")
        for key in seqs.keys():
            fo.write(key + "  ")
            fo.write(''.join(seqs[key]))
            fo.write('\n')
        fo.write("  ;\n")
        fo.write("End;\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--ms", type=str, default="ms",
                        help="Path to ms")

    parser.add_argument("-i", "--input", type=str, 
                        help="Input file (newick string with lengths in gens)",
                        required=True)

    parser.add_argument("-p", "--popsize", type=int, default=200000,
                        help="Effective population size")

    parser.add_argument("-l", "--nloci", type=int, default=1000000,
                        help="Number of independent loci")

    parser.add_argument("-s", "--nsites", type=int, default=1,
                        help="Number of sites per locus")

    parser.add_argument("-k", "--keep", type=int, default=100000,
                        help="Number of parsimony-informative sites to keep")

    parser.add_argument("-o", "--output", type=str,
                        help="Output", required=True)

    main(parser.parse_args())
