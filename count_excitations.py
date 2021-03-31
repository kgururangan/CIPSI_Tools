import numpy as np
import argparse
import sys
import os
from itertools import permutations as permutations

def is_excit(D,Dref,nexc_target):
		nexcit = len(set(D) - set(Dref))
		if nexcit==nexc_target:
				return True
		else:
				return False

def get_excits_from(D,Dref):
		return list(set(Dref) - set(D))

def get_excits_to(D,Dref):
		return list(set(D) - set(Dref))

def spatial_orb_idx(x):
		if x%2 == 1:
				return int( (x+1)/2 )
		else:
				return int( x/2 )

def main(args):

		nfroz = args.frozen
		nelec = args.electrons

		Dref = list(range(1,nelec+1))

		if os.path.isfile(args.infile):

			with open(args.infile) as f:

				#	ntrip = 0
				#	nquad = 0
					n_excit = np.zeros(nelec)

					for line in f.readlines():

							det = list(map(int,line.split()[2:]))
							p_occ = get_excits_from(det,Dref)
							p_unocc = get_excits_to(det,Dref)

							#print(p_occ)
							#print(p_unocc)
							if len(p_occ) > 0:
								excit_rank = len(p_occ)
								n_excit[excit_rank-1] += 1
							#if excit_rank == 3:
							#		ntrip += 1
							#if excit_rank == 4:
							#		nquad += 1
		else:
				print('File {} not found!. Exiting...'.format(args.infile))
				sys.exit()
		for i in range(len(n_excit)):
				print('Number of {}-tuple excitation = {}'.format(i+1,n_excit[i]))
	#	print('Number of Triples in P space = {}'.format(ntrip))
#		print('Number of Quadruples in P space = {}'.format(nquad))

if __name__ == '__main__':
		parser = argparse.ArgumentParser('Parser for writing the P space using a CIPSI list of CI vectors')
		parser.add_argument('-f','--frozen',type=int,default=0,
							help='Number of frozen spinorbitals')
		parser.add_argument('-n','--electrons',type=int,
							help='Number of correlated electrons')
		parser.add_argument('infile',type=str,
							help='CI vector file from CIPSI')
		args = parser.parse_args()
		main(args)


