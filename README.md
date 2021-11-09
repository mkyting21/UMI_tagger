<u>**UMI_tagger**</u>

Sequencing libraries generated using the "NEXTFLEX small RNA-seq kit V3" contain dual UMIs on the 5' and 3' end of the read.
UMI_tagger extracts these dual UMIs and formats the fastq file for UMI-tools (https://github.com/CGATOxford/UMI-tools).
UMI-tools can then perform PCR deduplication.

<ins>_INPUT FASTQ READ_</ins>:<br />
@NS500442:115:H77H7BGX7:1:11101:24207:1052 1:N:0:ATCACG <br />
**GGAC**ANAACGGGGTTGTGGGAGAGC**TAAC** <br />
\+ <br />
AAAAA#EEEAAEEE/EEEEAEEEEEEEEE <br />

<ins>_OUTPUT FASTQ READ_</ins>:<br />
@NS500442:115:H77H7BGX7:1:11101:24207:1052_**GGACTAAC** 1:N:0:ATCACG <br />
ANAACGGGGTTGTGGGAGAGC <br />
\+<br />
A#EEEAAEEE/EEEEAEEEEE<br />







UMI-tools can then read this barcode as **GGACTAAC**
