import numpy as np

# Expand Monomials From Number
#
# Description:
#	Given a number that encodes a monomial from a boolean polynomial, produces a list of
#	numbers that encode the resulting monomials in the corresponding numerical (mod 2)
#	polynomial. The list includes all monomials that result from 1) translating the 
#	boolean monomial into a term in numeric form and 2) fully expanding that term. 
#
# Inputs:
#	x - the specification of the monomial from the boolean polynomial. The 1 bits of x
#		correspond to bits that appear un-negated in the monomial. This encoding (and thus
#		this function) assumes that boolean monomials contain all bits, either negated or
#		un-negated.
#
#	n - the number of bits in the boolean polynomial
#
# Outputs:
#	monomials - the list of resulting numeric monomials 
#
# Requirements:
#	get_bit_inds from .

def expand_monomials_from_number(x,n):
	x_inds_0, _ = get_bit_inds(x,n)

	monomials = []
	# there is one monomial for each possible replacement of the set of zero bits in x
	# ... with a bit string; loop over the 2^|x_inds_0| possible bit strings
	for y in range(2**len(x_inds_0)):
		_, y_inds_1 = get_bit_inds(y,n)

		m = x
		# for any 1's in the replacement bit string, add its value to x
		#  ... according to the position of the original 0 bit in x
		for i in y_inds_1:
			m += 2**x_inds_0[i]
		monomials.append(m)

	return monomials
	
# ----------------------------------------------------------------------------------------	

# Get Bit Indices
#
# Description:
#	A helper function that, given a non-negative integer, returns the positions of the
#	0's and 1's the corresponding bit string.
#
# Inputs:
#	x - the integer
#
#	n - the number of bits in the bit string
#
# Outputs:
#	inds_0 - positions of the 0's in the binary representation of x
#
#	inds_1 - positions of the 1's in the binary representation of x
#
# Requirements:
#	numpy as np
	
	
def get_bit_inds(x,n):
	binary_list = [int(b) for b in np.binary_repr(x, n)[::-1]]
	inds_0 = [i for i,b in enumerate(binary_list) if b == 0]
	inds_1 = [i for i,b in enumerate(binary_list) if b == 1]
	
	return inds_0, inds_1
	
# ----------------------------------------------------------------------------------------	

# Monomial Mod 2
#
# Description:
#	Given a list of numbers that encodes monomials from a boolean polynomial, returns a
#	list of numbers that encodes the monomials from the corresponding numeric (mod 2)
#	polynomial.
#
# Inputs:
#	x_list - the list of monomial from the boolean polynomial
#
#	n - the number of bits in the boolean polynomial
#
# Outputs:
#	all_monomials_mod2 - a list of all monomials in the numerical polynomial, reduced
#		modulo 2
#
# Requirements:
#	expand_monomials_from_number from .

def get_monomials_mod2(x_list, n):
	all_monomials_mod2 = set()
	for x in x_list:
		for m in expand_monomials_from_number(x,n):
			if m in all_monomials_mod2:
				# if the monomial is already in the polynomial,
				# ... it's coefficent now becomes 0 (mod 2): remove it
				all_monomials_mod2.remove(m)
			else:
				# ... otherwise add it
				all_monomials_mod2.add(m)

	return list(all_monomials_mod2)


