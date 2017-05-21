# BLEU-score_calculation
Program to calculate the BLEU score for a corpus of translation data

Implement a program that calculates the BLEU evaluation metric as defined in [this paper](https://aclweb.org/anthology/P/P02/P02-1040.pdf). The program will run on set of candidate and reference translations, and will calculate the BLEU score for each candidate.

### Programs ###
Write a Python program - __calculatebleu.py__, which will take a two paths as parameters: the first parameter will be the path to the candidate translation (a single file), and the second parameter will be a path to the reference translations (either a single file, or a directory if there are multiple reference translations). The program will write an output file called __bleu_out.txt__ which contains a single floating point number, representing the BLEU score of the candidate translation relative to the set of reference translations. For example:

_python calculatebleu.py /path/to/candidate /path/to/reference_

The candidate and reference files have been provided with the following BLEU scores:

German      candidate-1.txt reference-1.txt - 0.151184476557
Greek       candidate-2.txt reference-2.txt - 0.0976570839819
Portuguese  candidate-3.txt reference-3.txt - 0.227803041867
English     candidate-4.txt (reference-4a.txt and reference-4b.txt) - 0.227894952018
