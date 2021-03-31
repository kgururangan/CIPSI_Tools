import sys
import os
import numpy as np



if __name__ == '__main__':

	fcidumppath = sys.argv[1]
	twobodypath = sys.argv[2]
	onebodypath = sys.argv[3]
	#Norb = int(sys.argv[4])
	#Nelec = int(sys.argv[5])
	#Nocc = int(Nelec/2)

	if not os.path.isfile(fcidumppath):
		print('File path {} does not exist. Exiting...'.format(fcidumppath))
		sys.exit()
	else:
		with open(fcidumppath) as fp:

		#	VVmat = np.zeros((Norb,Norb,Norb,Norb))
		#	Zmat = np.zeros((Norb,Norb))

			ct2body = 0
			ct1body = 0
			for ct, line in enumerate(fp.readlines()):

				if ct == 0:
					L = line.split()
				#	print(L[5])
					Norb = int(L[2])
					Nelec = int(L[5])
					Nocc = int(Nelec/2)
					VVmat = np.zeros((Norb,Norb,Norb,Norb))
					Zmat = np.zeros((Norb,Norb))

				if ct > 3: # skip initial stuff

					L = line.split()

					Cf = float(L[0])
					p = int(L[1])-1
					r = int(L[2])-1
					q = int(L[3])-1
					s = int(L[4])-1

			#		prqs = str(p)+str(r)+str(q)+str(s)
			#		print(prqs)

					if q !=-1 and s!= -1: # twobody term

						VVmat[p,r,q,s] = Cf
						VVmat[r,p,q,s] = Cf
						VVmat[p,r,s,q] = Cf
						VVmat[r,p,s,q] = Cf
						VVmat[q,s,p,r] = Cf
						VVmat[q,s,r,p] = Cf
						VVmat[s,q,p,r] = Cf
						VVmat[s,q,r,p] = Cf

			#			ct2body += 1

					elif q == -1 and s == -1 and p != -1: # onebody term
						Zmat[p,r] = Cf
						Zmat[r,p] = Cf

			#			ct1body += 1

					else: # nuclear repulsion
						Vnuc = Cf
		twobodyfile = open(twobodypath,'w')
		onebodyfile = open(onebodypath,'w')

		for i in range(Norb):
			for j in range(Norb):	
				if j <= i:
					ct1body += 1
					onebodyfile.writelines('  '+str(Zmat[i,j]).rjust(10,' '))
					onebodyfile.writelines('  '+str(ct1body).rjust(10,' '))
					onebodyfile.write('\n')
				for k in range(Norb):
					for l in range(Norb):
						twobodyfile.write('  ')
						twobodyfile.writelines(str(oc) for oc in [i+1,'  ',j+1,'  ',k+1,'  ',l+1])
						twobodyfile.write('  {:>24.18E}'.format(VVmat[i,j,k,l]))
						twobodyfile.write('\n')
		twobodyfile.write('  ')
		twobodyfile.writelines(str(oc) for oc in [0,'  ',0,'  ',0,'  ',0])
		twobodyfile.write('   '+str(Vnuc))

		twobodyfile.close()
		onebodyfile.close()


#################### PRINTING PERMUTATIONALLY UNIQUE INTEGRALS (NOT USED IN CCQ!) ##############################
#			for i in range(Norb):
#				for j in range(i+1):
#					ct1body += 1
#					onebodyfile.writelines('  '+str(Zmat[i,j]).rjust(10,' '))
#					onebodyfile.writelines('  '+str(ct1body).rjust(10,' '))
#					onebodyfile.write('\n')
#					for k in range(i+1):
#						if i == k:
#							lmax = j+1
#						else:
#							lmax = k+1
#						for l in range(lmax):
#							ct2body+=1
#
#							twobodyfile.write('  ')
#							twobodyfile.writelines(str(oc) for oc in [i+1,'  ', j+1,'  ', k+1,'  ', l+1])
#							twobodyfile.write('   '+str(VVmat[i,j,k,l]))
#							twobodyfile.write('\n')
#
#		twobodyfile.write('  ')
#		twobodyfile.writelines(str(oc) for oc in [0,'  ',0,'  ',0,'  ',0])
#		twobodyfile.write('   '+str(Vnuc))

#		print(ct2body)
#		twobodyfile.close()
#		onebodyfile.close()

###################### CHECKING SCF ENERGY, MUST MATCH CIPSI/CCQ OUTPUT! ###########################################
		VVmat = np.einsum('prqs->pqrs',VVmat)			# chemist to physics notation
		J = np.einsum('ijij->',VVmat[:Nocc,:Nocc,:Nocc,:Nocc])  # coulomb
		K = np.einsum('ijji->',VVmat[:Nocc,:Nocc,:Nocc,:Nocc])	# exchange
		H = np.einsum('ii->',Zmat[:Nocc,:Nocc])			# Hcore

		EHF = 2*H + 2*J - K
		Etot = EHF + Vnuc

#			print(ct2body)
#			print(ct1body)

#			VVmat2 = VVmat.copy()
#			for i in range(Norb):
#				for j in range(Norb):
#					for k in range(Norb):
#						for l in range(Norb):
#							if np.abs(VVmat2[i,j,k,l]) < 10**-10:
#								VVmat2[i,j,k,l] = 0.0
#			print(VVmat2)


		print('The electronic energy is {} Ha'.format(EHF))
		print('The nuclear repulsion energy is {} Ha'.format(Vnuc))
		print('The total energy is {} Ha'.format(Etot))				

