#!/usr/bin/python
#USAGE: ./UMI_tagger.py [file_name]
#[file_name] can be ".fastq" or ".fastq.gz" format, but the output will be .fastq
####################################################################################################################################################
#Author: Michael Ting
#edited 2021-11-1
#Description: This python script will process dual UMIs generated from the "NEXTflex small RNA-seq V3 kit", and prepare fastq files for UMI-Tools (https://github.com/CGATOxford/UMI-tools)
	#It works by trimming the first four & last four nucleotides and tagging them to the read name

####################################################################################################################################################
#e.g. the fastq read becomes:
	#@NS500442:115:H77H7BGX7:1:11101:24207:1052 1:N:0:ATCACG
	#GGACANAACGGGGTTGTGGGAGAGCTAAC
	#+
	#AAAAA#EEEAAEEE/EEEEAEEEEEEEEE

	#@NS500442:115:H77H7BGX7:1:11101:24207:1052_GGACTAAC 1:N:0:ATCACG
	#ANAACGGGGTTGTGGGAGAGC
	#+
	#A#EEEAAEEE/EEEEAEEEEE

#umi_tools can then read this barcode as GGACTAAC
####################################################################################################################################################

#used for calculatingprocessing time
import time
start = time.time()
import sys
#use of regular expressions
import re
#reading gzipped files so I don't have to unzip fastq files
import gzip

#define general function for trimming umi and adding it to the 'fastq header'
def process_umi():
	#fastq files have 4 lines. The script will act differently according to which line it is.
	readname_count = 1
	sequence_count = 2
	optional_count = 3
	quality_count = 4

	for linenumber, line in enumerate(handle, start = 1):
		#fastq line#1: Storing the header as variable for manipulation
		if linenumber == readname_count:
			temp_readname = line.strip()
			#e.g. pattern im trying to capture -> @NS500442:115:H77H7BGX7:1:11101:24207:1052 1:N:0:ATCACG
			match = re.search(r'(@[\w:]*)(\s[\w:]*)', temp_readname)
			if match:
				header_start = match.group(1)
				header_end = match.group(2)
			readname_count += 4
		#fastq line#2: Storing the sequence as variable for manipulation
		elif linenumber == sequence_count:
			temp_sequence = line.strip()
			#use regular expressions to capture UMI on the 5' end of sequence
			FiveprimeUMI = re.search(r'^[ATCGN]{4}', line)
			if FiveprimeUMI:
				umi1 = FiveprimeUMI.group()
			ThreeprimeUMI = re.search(r'[ATCGN]{4}$', line)
			if ThreeprimeUMI:
				umi2 = ThreeprimeUMI.group()
			#add the 2 umi's to the temporary 'header', then write the trimmed sequence
			newfile.write(header_start + '_' + umi1 + umi2 + header_end + "\n")
			newfile.write(temp_sequence[4:-4] + "\n")
			sequence_count += 4
		#fastq line#3: optional line
		elif linenumber == optional_count:
			newfile.write(line.strip() + "\n")
			optional_count += 4
		#fastq line#4: Storing quality score as variable-> also trimming quality scores to match trimmed sequence
		elif linenumber == quality_count:
			newfile.write(line.strip()[4:-4] + "\n")
			quality_count += 4

#sys.argv allows you to store input from STDIN as a variable
file_name=sys.argv[1]

#choose if the file is gzipped or unzipped
match0 = re.search(r'\.gz', file_name)
if match0:
	#Create "newfile" to append the umi sequences. To make the name cleaner, trim the ".gz" from the file_name
	newfile = open("umi_%s" %file_name[:-3], "a+")
	#read the gzipped fastq file and process it according to the function "process_umi"
	with gzip.open(file_name, 'rb') as handle:
		process_umi()
else:
	#Create "newfile" to append the umi sequences.
	newfile = open("umi_%s" %file_name, "a+")
	#read the fastq file and process it according to the function "process_umi"
	with open(file_name, 'r') as handle:
		process_umi()
			
end = time.time()
newfile.close()

#keeps a record of processing time in seconds
print "processing time"
print(end - start)
