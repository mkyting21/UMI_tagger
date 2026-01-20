<u>**UMI_tagger**</u>
Identifies 5' and/or 3' UMIs and tags them to the fastq header. This formats the fastq file as input for UMI-tools (https://github.com/CGATOxford/UMI-tools), for PCR deduplication.

<ins>_INPUT FASTQ READ_</ins>:<br />
@NS500442:115:H77H7BGX7:1:11101:24207:1052 1:N:0:ATCACG <br />
<u>**GGAC**<u>ANAACGGGGTTGTGGGAGAGC<u>**TAAC**<u> <br />
\+ <br />
AAAAA#EEEAAEEE/EEEEAEEEEEEEEE <br />

<ins>_OUTPUT FASTQ READ_</ins>:<br />
@NS500442:115:H77H7BGX7:1:11101:24207:1052_<u>**GGACTAAC**<u> 1:N:0:ATCACG <br />
ANAACGGGGTTGTGGGAGAGC <br />
\+<br />
A#EEEAAEEE/EEEEAEEEEE<br />







UMI-tools can then read this barcode as **GGACTAAC**
