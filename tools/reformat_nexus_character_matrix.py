"""
Reformat nexus matrix for Dollo-CDP
"""
import argparse
import sys

class CharacterMatrix():
    def __init__(self, ntax, nchar, taxlabels, data):
        self.ntax = ntax
        self.nchar = nchar
        self.taxlabels = taxlabels
        self.data = data

    def __init__(self, inputf):
        if self.istranposed(inputf):
            self.read_tranposed_matrix(inputf)
        else:
            sys.exit("Can only read tranposed matrices!\n")

    def istranposed(self, inputf):
        with open(inputf, 'r') as fp:
            for line in fp:
                line = line.replace(';', '')
                words = line.split()
                if len(words) == 0:
                    continue
                if words[0] == "format":
                    if words[1] == "transpose":
                        return True
                elif words[0] == "matrix":
                    return False
        return False

    def read_tranposed_matrix(self, inputf):
        with open(inputf, 'r') as fp:
            for line in fp:
                tmp = line.replace(';', '')
                words = tmp.split()
                if len(words) == 0:
                    continue
                if words[0] == "dimensions":
                    self.ntax = int(words[1].replace("ntax=", ''))
                    self.nchar = int(words[2].replace("nchar=", ''))
                elif words[0] == "taxlabels":
                    self.taxlabels = words[1:]
                elif words[0] == "matrix":
                    break

            self.data = []
            for ind in range(self.ntax):
                self.data.append("")

            for line in fp:
                words = line.split()
                if words[0].find(';') > -1:
                    break
                for ind, state in enumerate(words[1]):
                    self.data[ind] += state

    def write(self, outputf):
        with open(outputf, 'w') as fp:
            fp.write("#NEXUS\n\n")
            fp.write("Begin data;\n")
            fp.write("\tDimensions ntax=%d nchar=%d;\n" % (self.ntax, self.nchar))
            fp.write("\tFormat datatype=standard gap=-;\n")
            fp.write("\tMatrix\n")
            for ind in range(self.ntax):
                fp.write(self.taxlabels[ind] + ' ' + self.data[ind] + '\n')
            fp.write('\t;\n')
            fp.write("End;\n")


def main(args):
    cmat = CharacterMatrix(args.input)
    cmat.write(args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Input nexus file containing character matrix")

    parser.add_argument("-o", "--output", type=str, required=False,
                        help="Output nexus file")

    main(parser.parse_args())

