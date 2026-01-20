# <u>**UMI_tagger**</u>
Identifies 5' and/or 3' UMIs and tags them to the fastq header. This formats the fastq file as input for UMI-tools (https://github.com/CGATOxford/UMI-tools), for PCR deduplication.

## Example usage:
If you have a fastq file with 4nt UMIs on the 5' and 3' side, you would run:
```
python UMI_tagger.py -5p 4 -3p 4 File.fastq
```

#### fastq input
```
@NS500442:115:H77H7BGX7:1:11101:24207:1052 1:N:0:ATCACG 
GGACANAACGGGGTTGTGGGAGAGCTAAC
+ 
AAAAA#EEEAAEEE/EEEEAEEEEEEEEE 
```

#### fastq output
```
@NS500442:115:H77H7BGX7:1:11101:24207:1052_GGACTAAC 1:N:0:ATCACG 
ANAACGGGGTTGTGGGAGAGC
+ 
A#EEEAAEEE/EEEEAEEEEE
```
