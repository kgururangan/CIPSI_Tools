# CIPSI_Tools
Collection of scripts that are used to parse and manipulate CIPSI wavefunctions generated using Quantum Package 2.0. These codes were used in ongoing research on selected-CI-driven CC(P;Q) and externally corrected coupled-cluster (ec-CC) methods. For more information, please see the papers

I. Magoulas, K. Gururangan, P. Piecuch, J. E. Deustua, and J. Shen, arXiv e-prints, arXiv:2102.10143 (2021), arXiv:2102.10143 [physics.chem-ph]

K. Gururangan, J. E. Deustua, J. Shen, and P. Piecuch, In Preparation.

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
parse_fcidump.py

usage: parse_fcidump.py [-h] [-1 ONEBODYPATH] [-2 TWOBODYPATH] [--fcidumppath FCIDUMPPATH]

Parser to extract onebody and twobody integrals from the QP2 fcidump file

optional arguments:
  -h, --help            show this help message and exit
  -1 ONEBODYPATH, --onebodypath ONEBODYPATH
                        File name for output onebody integrals
  -2 TWOBODYPATH, --twobodypath TWOBODYPATH
                        File name for output twobody integrals
  --fcidumppath FCIDUMPPATH
                        File name of QP2 fcidump
```
Parses the contents of the FCIDUMP file produced from a QP2 calculations via the command ```qp_run fcidump *.ezfio```. Remember to freeze orbitals prior to running FCIDUMP.

```
count_excitations.py

usage: Parser for counting the excitations of all ranks in a CIPSI wavefunction. [-h] [-f FROZEN] [-n ELECTRONS] infile

positional arguments:
  infile                CI vector file from CIPSI

optional arguments:
  -h, --help            show this help message and exit
  -f FROZEN, --frozen FROZEN
                        Number of frozen spinorbitals
  -n ELECTRONS, --electrons ELECTRONS
                        Number of correlated electrons
  ````
Counts the number of excitations contained within a CIPSI wavefunction of all ranks (up to N, where N is the number of correlated electrons). The CI vector file is the ASCII output file from ```parse_ci_vectors.py```.

```
write_p_space.py

usage: Parser for writing the P space using a CIPSI list of CI vectors [-h] [-f FROZEN] [-n ELECTRONS] [-e EXCITATION] infile

positional arguments:
  infile                CI vector file from CIPSI

optional arguments:
  -h, --help            show this help message and exit
  -f FROZEN, --frozen FROZEN
                        Number of frozen spinorbitals
  -n ELECTRONS, --electrons ELECTRONS
                        Number of correlated electrons
  -e EXCITATION, --excitation EXCITATION
                        Excitation rank of P space
 ```
Writes a file containing the spinorbital strings ```(a_1, a_2, ... a_k, i_1, i_2, ... i_k)``` for the subspace of the P space containing all excitations of rank k 
captured by the CIPSI wavefunction. The CI vector file is the ASCII output file from ```parse_ci_vectors.py```. This P space file is used for subsequent CC(P) calculations and CC(P;Q) moment corrections.
