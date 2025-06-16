import numpy as np

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
	
	
def get_bit_inds(x,n):
	binary_list = [int(b) for b in np.binary_repr(x, n)[::-1]]
	inds_0 = [i for i,b in enumerate(binary_list) if b == 0]
	inds_1 = [i for i,b in enumerate(binary_list) if b == 1]
	
	return inds_0, inds_1
	
	
# ----------------------------------------------------------------------------------------	

def get_monomials_mod2(x_list, n):
	all_monomials_mod2 = set()
	for x in x_list:
		for m in expand_monomials_from_number(x,n):
			if m in all_monomials_mod2:
				# if the monomial is already in the polynomial, it's coefficent now becomes 0 (mod 2): remove it
				all_monomials_mod2.remove(m)
			else:
				# ... otherwise add it
				all_monomials_mod2.add(m)

	return list(all_monomials_mod2)


