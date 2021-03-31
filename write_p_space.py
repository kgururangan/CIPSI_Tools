import numpy as np
import sys
import os
import argparse
from itertools import permutations as permutations

def is_triple_excit(D,Dref):
		nexcit = len(set(D) - set(Dref))
		if nexcit==3:
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
		excit_target = args.excitation
	#	nstates = args.states

		occ_lowb = spatial_orb_idx(nfroz) + 1
		occ_upb = spatial_orb_idx(nelec+nfroz)

		unocc_lowb = occ_upb + 1
		#unocc_upb = Number of spatial orbitals total

		Dref = list(range(1,nelec+1))

		if os.path.isfile(args.infile):

			with open(args.infile) as f:

					f_target = open(args.infile+'-p','w')
					f_target_long = open(args.infile+'-p-long','w')
					ntrip = 0
					outstring = '{:>3}'*(2*excit_target)
					for line in f.readlines():

							det = list(map(int,line.split()[2:]))
						#	det = list(map(int,line.split()[nstates+1:]))
							p_occ = get_excits_from(det,Dref)
							p_unocc = get_excits_to(det,Dref)
			
							excit_rank = len(p_occ)
							if excit_rank == excit_target:
									ntrip += 1

									p_occ_2 = [spatial_orb_idx(p_occ[i]+nfroz) for i in range(excit_rank)]
									p_unocc_2 = [spatial_orb_idx(p_unocc[i]+nfroz) for i in range(excit_rank)]
									
									if any(np.asarray(p_occ_2) > occ_upb) or any(np.asarray(p_occ_2) < occ_lowb):
											print('Occupied orbitals out of range!')
											sys.exit()
									if any(np.asarray(p_unocc_2) < unocc_lowb):
											print('Unoccupied orbitals out of range!')
											sys.exit()

									f_target_long.writelines('Determinant #{}: '.format(ntrip))
									f_target_long.writelines(' %s  ' % s for s in det)
									f_target_long.writelines('\n')
									f_target_long.writelines('Occupied: ')
									f_target_long.writelines(' %s  ' % s for s in p_occ_2)
									f_target_long.writelines('\n')
									f_target_long.writelines('Unoccupied: ')
									f_target_long.writelines(' %s  ' % s for s in p_unocc_2)
									f_target_long.writelines('\n')

									for I in permutations(p_occ_2):
											for A in permutations(p_unocc_2):

													f_target.write(outstring.format(*list(A),*list(I)))
													f_target.write('\n')

					f_target.close()
					f_target_long.close()
					f.close()
		else:
				print('File {} not found! Exiting...'.format(args.infile))
				sys.exit()

if __name__ == '__main__':
		parser = argparse.ArgumentParser('Parser for writing the P space using a CIPSI list of CI vectors')
		parser.add_argument('-f','--frozen',type=int,default=0,
							help='Number of frozen spinorbitals')
		parser.add_argument('-n','--electrons',type=int,
							help='Number of correlated electrons')
		parser.add_argument('-e','--excitation',type=int,default=3,
							help='Excitation rank of P space')
	#	parser.add_argument('-s','--states',type=int,default=1,
#							help='Number of states in calculation (including ground!)')
		parser.add_argument('infile',type=str,
							help='CI vector file from CIPSI')
		args = parser.parse_args()
		main(args)


