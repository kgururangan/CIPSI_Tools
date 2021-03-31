import sys
import os
import numpy as np
import argparse

def hextobin(hex_string):
	bin_string = bin(int(hex_string,16))[2:]
	return bin_string

def signPermutation(p):
 # explicitly using cycle notation of permutation
 # input: p is a list of permutation indices 
 # i.e. [x_sorted, p] = sort(x_unsorted)

	n = len(p)
	visited = [False]*n
	sign = 1
	for k in range(n):
		if (not visited[k]):
			ct = k
			L = 0
			while (not visited[ct]):
				L += 1
				visited[ct] = True
				ct = p[ct]
			if L%2 == 0:
				sign = -1*sign
	return sign
	

 
def main(args):

#	infilepath = sys.argv[1]
#	outfilepath = sys.argv[2]
#	nfroz = int(sys.argv[3])
	
	infilepath = args.infilepath
	outfilepath = args.outfilepath
	nfroz = args.frozen
	flag_intnorm = args.flag_intnorm
	flag_froz_shift = args.froz_shift

	if not os.path.isfile(infilepath):
		print("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()

	with open(infilepath) as fp:

		outFile = open(outfilepath,'w')	

		lines = fp.readlines()
		cnt = 0
		mm = 4
		for j in range(len(lines)-mm):
			line = lines[j]
			linestrip = line.split()
			if 'Determinant' in linestrip:

				iocc_alpha = []
				iocc_beta = []		

				next_line_split = lines[j+1].split('|')
				coef_line = lines[j+mm].split()
				alpha = hextobin(next_line_split[0])[::-1]
				beta = hextobin(next_line_split[1])[::-1]

				if cnt == 0:
					coef_HF = float(coef_line[0])

				iocc_alpha = [2*i+1 for i in range(len(alpha)) if alpha[i] == '1']
				iocc_beta = [2*i+1+1 for i in range(len(beta)) if beta[i] == '1']
				iocc0 = iocc_alpha + iocc_beta
				idx_perm = list(np.argsort(iocc0))
				iocc = [iocc0[idx_perm[i]] for i in range(len(iocc0))]				

				# Must find the sign of the permuation associated with the list sort function
				sign = signPermutation(idx_perm)

				iocc_correlate = [int(float(iocc[i+nfroz])-float(nfroz)) for i in range(len(iocc)-nfroz)]
				if flag_froz_shift:
						iocc_correlate = [x + nfroz for x in iocc_correlate]
				if flag_intnorm:
					outLine = [cnt+1,sign*float(coef_line[0])/coef_HF] + iocc_correlate
				else:
					outLine = [cnt+1, sign*float(coef_line[0])] + iocc_correlate
			
				outFile.write('    ')	
				outFile.writelines(str(oc).ljust(10,' ') for oc in outLine[:1])
				outFile.writelines(str(oc).ljust(20,' ') for oc in outLine[1:2])
				outFile.write('    ')
				outFile.writelines(str(oc).ljust(4,' ') for oc in outLine[2:])
				outFile.write("\n")				

				cnt+=1

		outFile.close()


if __name__ == '__main__':
# only runs these lines if you are executing file directly
# python fci_text_parse_v1 INFILE OUTFILE NFROZ | tee ci.vectors.out
# ./

	#q = [0,1,2]
	#print(signPermutation(q))

	#q = [1,0,2]
	#print(signPermutation(q))

	#q = [2,1,0]
	#print(signPermutation(q))

	parser = argparse.ArgumentParser(description="CIPSI CI vector output parser")
	parser.add_argument('-f','--frozen',type=int,
						help='Number of frozen electrons')
	parser.add_argument('infilepath',type=str,
						help='File path of CIPSI CI vector output file')
	parser.add_argument('-o','--outfilepath',type=str,default='ci.vectors.dat',
						help='Output file name. Default is ci.vectors.dat')
	parser.add_argument('-s','--froz_shift',type=bool,default=False,
						help='True/False boolean. If False (default), numbers correlated electrons starting from 1. If True, numbers correlated electrons							    starting from nfroz + 1')
	parser.add_argument('-i','--flag_intnorm',type=bool,default=False, help='True/False flag for whether or not to print CI coefficients in intermediate normalization')
	args = parser.parse_args()
	main(args)







