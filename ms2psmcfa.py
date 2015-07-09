#!/usr/bin/env python

import sys, argparse

parser = argparse.ArgumentParser(description="Converts the output of MS into \
                                    psmcfa format (the input file of psmc)")
parser.add_argument("-s", "--bin_size", type=int, default=100, 
                    help="The equivalent of bin_size in psmc")
parser.add_argument("input_ms_results", help="The file produced by MS")

# Read the input from the command line
args = parser.parse_args()
BinSize = args.bin_size
fname = args.input_ms_results

# Read the file
with open(fname, 'r') as f:
    ms_out_text = f.read()

ms_command = ms_out_text[:ms_out_text.index('\n')]
# Compute the total length of the simulated sequence
SeqLength = int(ms_command.split(' -r ')[1].split(' ')[1])

# Compute the number of bins (see PSMC documentation)
nBins = int(SeqLength / BinSize) + (SeqLength%BinSize != 0)

sequences_list = ms_out_text.split('segsites: ')[1:]
count = 0

for seq in sequences_list:
    count += 1
    (segsites, positions_list) = seq.split('\n')[:2]
    segsites = int(segsites)
    positions_list = positions_list.split()[1:]
    # Start by a sequence of length nBins with all positions being 
    # heterozigous. As long as we find a SNP position, we compute the 
    # place in the sequence and we marked with 'K'
    A=['T'] * nBins
    for p in positions_list:
        pos = int(float(SeqLength) * float(p) / BinSize )
        A[pos] = 'K'
    sys.stdout.write(">{}\n".format(count))
    # Split the sequence in lines of 60 characters and send them to the
    # standart output
    for i in range(len(A)):
        if i>0 and i%60==0:
            sys.stdout.write('\n')
        sys.stdout.write(A[i])
    sys.stdout.write('\n')
