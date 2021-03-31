# CIPSI_Tools
Collection of scripts that are used to parse and manipulate CIPSI wavefunctions generated using Quantum Package 2.0. These codes were used in ongoing research on selected-CI-driven CC(P;Q) and externally corrected coupled-cluster (ec-CC) methods.

Content Descriptions:

```
parse_ci_vectors.py

usage: python parse_ci_vectors.py [-h] [-f FROZEN] [-o OUTFILEPATH] [-s FROZ_SHIFT] [-i FLAG_INTNORM] infilepath

CIPSI CI vector output parser

positional arguments:
  infilepath            File path of CIPSI CI vector output file

optional arguments:
  -h, --help            show this help message and exit
  -f FROZEN, --frozen FROZEN
                        Number of frozen electrons
  -o OUTFILEPATH, --outfilepath OUTFILEPATH
                        Output file name. Default is ci.vectors.dat
  -s FROZ_SHIFT, --froz_shift FROZ_SHIFT
                        True/False boolean. If False (default), numbers correlated electrons starting from 1. If True, numbers correlated electrons starting
                        from nfroz + 1
  -i FLAG_INTNORM, --flag_intnorm FLAG_INTNORM
                        True/False flag for whether or not to print CI coefficients in intermediate normalization
```
Parses the contents of the CI vectors from a CIPSI wavefunction and outputs them in an ASCII file that is compatible with CC(P;Q) and ec-CC codes developed in the Piecuch group. In the function call, ```infilepath``` is a file generated using the command ```qp_run print_ci_vectors *.ezfio``` in Quantum Package 2.0



```
parse_ci_vectors.py
Parses the contents of the CI vectors from a CIPSI wavefunction and outputs them in an ASCII file that is compatible with CC(P;Q) and ec-CC codes developed in the Piecuch group
```
