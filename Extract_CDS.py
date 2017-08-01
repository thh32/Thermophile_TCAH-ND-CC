import HTSeq
import argparse

def rev_comp(sequence):
    original = sequence
    wanted = []
    for i in reversed(list(sequence.upper())):
        if i == 'A':
            wanted.append('T')
        elif i == 'T':
            wanted.append('A')
        elif i == 'C':
            wanted.append('G')
        elif i == 'G':
            wanted.append('C')

    new_seq = ''.join(wanted)
    return new_seq
        



parser = argparse.ArgumentParser() #simplifys the wording of using argparse as stated in the python tutorial


# Basic input output files
parser.add_argument("-i", type=str, action='store',  dest='input', help="Input the FASTA/Q file") # allows input of the forward read
parser.add_argument("-g", type=str, action='store',  dest='gffinput', help="Input the GFF file") # allows input of the forward read
parser.add_argument("-o", type=str, action='store',  dest='output', help="Name for the output files") # allows input of the forward read
parser.add_argument("-t", type=str, action='store',default= 'CDS',  dest='extraction', help="Choose if CDS or custom region to be extracted")


# Input file type
parser.add_argument('-fasta', action='store_true', default=False, dest='fasta_switch', help='Input is fasta')
parser.add_argument('-fastq', action='store_true', default=False, dest='fastq_switch', help='Input is fastq')


args = parser.parse_args()



# Place each of the input into a simple variable to call
seq_file = str(args.input)
GFF_file = str(args.gffinput)
outputfile = str(args.output)
wanted = str(args.extraction)

fasta = False
if args.fasta_switch == True:
    fasta = True

fastq = False
if args.fastq_switch == True:
    fastq = True


cds_dic = {}

for line in open(GFF_file,'r'):
    if line.startswith('#') or line == '\n':
        continue
    else:
        timber = line.split('\t')
        #print timber
        contig = timber[0]
        cds_or_not = timber[2]
        if cds_or_not == 'CDS':
            strand = timber[6]
            start = int(timber[3])
            end = int(timber[4])
            if contig in cds_dic:
                prev = cds_dic[contig]
                prev[str(start) + '...' + str(end)] = strand
            else:
                temp = {}
                temp[str(start) + '...' + str(end)] = strand
                cds_dic[contig] = temp










outputting = open(outputfile,'w')

if fasta == True:
    for read in HTSeq.FastaReader(seq_file):
        if read.name in cds_dic.keys():
            cds_needed = cds_dic[read.name]
            for k,v in cds_needed.iteritems():
                start = int(k.split('...')[0])-1
                end = int(k.split('...')[1])
                stand = v
                where2end = len(read.seq) - end
                cds = read.seq[start:-where2end]
                if stand == '+':
                    outputting.write('>' + k + '.' + strand +'\n')
                    outputting.write(cds + '\n')
                if stand == '-':
                    corrected = rev_comp(cds)
                    outputting.write('>' + k + '.' + strand +'\n')
                    outputting.write(corrected + '\n')
elif fastq == True:
    for read in HTSeq.FastqReader(seq_file):
        if read.name in cds_dic.keys():
            cds_needed = cds_dic[read.name]
            for k,v in cds_needed.iteritems():
                start = int(k.split('...')[0])-1
                end = int(k.split('...')[1])
                stand = v
                where2end = len(read.seq) - end
                cds = read.seq[start:-where2end]
                if stand == '+':
                    outputting.write('>' + k + '.' + strand +'\n')
                    outputting.write(cds + '\n')
                if stand == '-':
                    corrected = rev_comp(cds)
                    outputting.write('>' + k + '.' + strand +'\n')
                    outputting.write(corrected + '\n')
else:
    print 'FILE TYPE NOT DEFINED; type either "fasta" or "fastq"'
    
outputting.close()

