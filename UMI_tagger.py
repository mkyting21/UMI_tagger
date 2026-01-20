"""
Author: Michael Ting
Date: 2026-1-17
Notes: UMI_tagger clips 5p and 3p UMIs, and tags them to the read ID
"""

import sys
import gzip
import re
import argparse
from tqdm import tqdm
from pathlib import Path 
from Bio.SeqIO.QualityIO import FastqGeneralIterator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "UMI_tagger: Tags Unique Molecular Identifiers (UMI) to fastq read name (Required setup for UMI_tools)")
    parser.add_argument("file", type=str, help = "fastq file") #positional arg
    parser.add_argument("-5p", "--umi_length_5p", metavar= "Length", type=int, help="nt length of 5prime UMI. Can be used with -3p", default = 0)
    parser.add_argument("-3p", "--umi_length_3p", metavar = "Length", type=int, help="nt length of 3prime UMI. Can be used with -5p", default = 0)
    parsed_args = parser.parse_args()

#extract variables from args
umi_length_5p=parsed_args.umi_length_5p
umi_length_3p=parsed_args.umi_length_3p
input_file=parsed_args.file

#Exit if no UMIs were entered
if umi_length_5p + umi_length_3p == 0:
    sys.exit("ERROR: No UMI info was entered. Please enter value(s) for '-5p' and/or '-3p'")

#set variables for slicing the sequences. If no 3p umi was selected, set to "None" 
start = umi_length_5p
end = -umi_length_3p if umi_length_3p > 0 else None

#Function for handling file if it is .gz
def modified_open(filename, mode='rt'):
    if filename.endswith('.gz'):
        return gzip.open(filename, mode)
    else:
        return open(filename, mode)

#Name output file
output_file = re.sub(r'\.fastq.*', r'_UMI.fastq', input_file)
print(f"Converting {input_file} to {output_file}")
fastq_counter=0 #record number of fastq entries

with modified_open(input_file) as in_handle:
    with open(output_file, "w") as out_handle: 
        for header, seq, quality in tqdm( FastqGeneralIterator(in_handle),  desc="Processing" ):
            #identify umi sequences    
            umi_5p=seq[:umi_length_5p]             
            umi_3p=seq[-umi_length_3p:] if umi_length_3p > 0 else ""
            umi_full=umi_5p + umi_3p       

            #trim UMIs from sequence
            new_seq=seq[start:end]            

            #add umi to header
            temp_header=header.split(" ")
            temp_header[0]=f"{temp_header[0]}_{umi_full}"
            new_header=" ".join(temp_header)

            #trim the quality scores
            new_quality=quality[start:end]
    
            #save the modified fastq entry
            out_handle.write("@%s\n%s\n+\n%s\n" % (new_header, new_seq, new_quality) )
            fastq_counter += 1 

print(f"Total fastq entries: {fastq_counter}")

