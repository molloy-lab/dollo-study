import argparse

def main(input_file, output_file):
    ntax = 0
    nchar = 0
    taxons = set()
    dic = {}
    with open(input_file, 'r') as f1:
        for line in f1:
            [x, y] = line.split(',(')
            x = x[1:]
            list0 = x.split(',')
            y = y[:-3]  
            list1 = y.split(',')
            taxons.update(list0)
            taxons.update(list1)
            nchar += 1
        ntax = len(taxons)
        for i in range(nchar):
            dic[i] = {}
            for t in taxons:
                dic[i][t] = '?'
        curr = 0
    
    with open(input_file, 'r') as f1:
        for line in f1:
            [x, y] = line.split(',(')
            x = x[1:]
            list0 = x.split(',')
            y = y[:-2]
            list1  = y.split(',')
            for e in list0:
                dic[curr][e] = 0
            for e in list1:
                dic[curr][e] = 1
            curr += 1
    
    with open(output_file, 'w') as f2:
        f2.write('#NEXUS\n')
        f2.write('\n')
        f2.write('Begin data;\n')
        f2.write('\tDimensions ntax={} nchar={};\n'.format(ntax, nchar))
        f2.write('\tFormat datatype=standard gap=-;\n')
        f2.write('\tMatrix\n')
        
        for e in taxons:
            f2.write(e + ' ' + ' ')
            for i in range(nchar):
                f2.write('{}'.format(dic[i][e]))
            f2.write('\n')
        f2.write('\t;\n')
        f2.write('End;')








if __name__ == "__main__":
    parser = argparse.ArgumentParser();

    parser.add_argument("-i", '--input', type=str, help="Input file", required=True)

    parser.add_argument("-o", '--output', type=str, help="Output file", required=True)

    args = parser.parse_args()

    main(args.input, args.output)
