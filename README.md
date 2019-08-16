# RMIT CSIT CT JFLAP PDA Converter

## Background
The JFLAP automaton simulator used in teaching RMIT Computing Theory does not
allow a PDA to have an accepting condition of both final state and empty stack
by default. However, this can be simulated by adding a new final state and 
adding a transition from all existing final states with the transition function 
`lambda1, Z, lambda2`where `lambda1` is a empty read and `Z` is popping the starting stack 
and `lambda2` is an empty push.

## Prerequisites

1. Python Version 2 or 3, with standard packages: `os`, `argparse` and `xml.etree.ElementTree`.


## Running the script

This script is intended to assist with marking student submissions. 

```
$ python pda_converter.py <pda-in>.jff <pda-out>.jff
```

WARNING: if `pda-in` == `pda-out`, the conversion will be destructive.

For help, use `-h` option:

```
~/local/latest/dev/rmit_ct_pda_converter$python pda_converter.py -h
usage: pda_converter.py [-h] pda-in pda-out

Convert a PDA with Final States to a PDA with only one new final state and
additional transitions lambda, Z, lambda from all previous final states to
that new final state.Note it does NOT check the encoding of the files or their
types (text or JFLAP).

positional arguments:
  pda-in      .jff file containing the PDA to be converted
  pda-out     .jff file this script will output to

optional arguments:
  -h, --help  show this help message and exit
```


### Example of running against an example pda:
```
~/local/latest/dev/rmit_ct_pda_converter$python pda_converter.py ./samples/PDA-example.jff ./test-out.jff
~/local/latest/dev/rmit_ct_pda_converter$

```
