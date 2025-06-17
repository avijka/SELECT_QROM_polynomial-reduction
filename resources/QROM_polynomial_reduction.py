from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
from .polynomial_reduction_mod2 import *

# QROM Reduced Circuit
#
# Description:
#	Produces a Qiskit circuit that implements a SELCECT-style QROM for the given function
#	f. Aims to minimize the number of 'control points' in the circuit, i.e. the total
#	number of control qubits across all multi-controlled X gates, by representing f as
#	an polynomial and reducing it mod 2. This implementation is limited to polynomial
#	representations where each input bit only appears either negated or un-negated.
#
# Inputs:
#	f_1_list - the specification of the function f: a list of non-negative integers
#		between 0 and 2^n - 1, whose n-bit binary representation are the bit strings that
#		give f=1.
#
#	n - the number of input qubits
#
#	optimize_flips (optional, defaults to True) - if True, the function will perform a
#		brute-force search over of all possible sets of negations ('flips') of the input
#		qubits such that the number of control points in the circuit is minimized.
#
#	flip_spec (optional, only relevant if optimize_flips == False, defaults to 0])
#		- a non-negative integer, whose n-bit binary representation identifies which input
#		qubits should be flipped, if not determined by the optimize procedure
#
# Outputs:
#	qrom_qc - the QROM circuit
#
# Requirements:
#	QuantumCircuit, QuantumRegister, AncillaRegister from qiskit.circuit
#	get_monomials_mod2 from .polynomial_reduction_mod2
#	brute_force_flips from .

def get_QROM_reduced_circuit(f_1_list, n, optimize_flips = True, flip_spec = 0):
	
	# if desired, run brute-force optimization over possible flips of input bits
	if optimize_flips:
		flip_spec, _ = brute_force_flips(f_1_list, n)
		
	# get indices for qubits to be flipped
	_, flip_inds = get_bit_inds(flip_spec,n)
	
	# convert values in f_1_list to get the effective 
	x_vals = [x^flip_spec for x in f_1_list]

	# initialize circuit
	x_reg = QuantumRegister(size=n, name='x')
	y_reg = AncillaRegister(size=1, name='y')
	qrom_qc = QuantumCircuit(x_reg, y_reg, name='QROM')
	
	# flip the desired input qubits
	qrom_qc.x(x_reg[flip_inds])
	
	# get reduced polynomial and loop over its constituent monomials
	for m in get_monomials_mod2(x_vals, n):
	
		if m ==0: # if m=0, this is the constant monomial 1; its addition just negates f
			qrom_qc.x(y_reg[0]) # ... so apply NOT to the output bit
			
		else: # otherwise, the monomial involves some of the input bits
			# ... specifically, it involves x_k if the kth bit of the number m is 1
			_, inds_1 = get_bit_inds(m,n)
			
			# ... so apply a multi-controlled X controlled by those x_k
			qrom_qc.mcx(x_reg[inds_1], y_reg[0])
			
	# un-flip the input qubits originally flipped
	qrom_qc.x(x_reg[flip_inds])
	
	return qrom_qc	
	
	
# ----------------------------------------------------------------------------------------	

# Control Count
#
# Description:
#	Given a function f (specified as in get_QROM_reduced_circuit above), returns the total
# 	number of 'control points' in the corresponding QROM circuit, assuming no input bit 
#	flips. 
#
# Inputs:
#	f_1_list - the specification of the function f: a list of non-negative integers
#		between 0 and 2^n - 1, whose n-bit binary representation are the bit strings that
#		give f=1.
#
#	n - the number of input qubits
#
# Outputs:
#	num_controls - the number of control points
#
# Requirements:
#	get_monomials_mod2 and get_bit_inds from .polynomial_reduction_mod2


def get_control_count(f_1_list, n):
	monomials = get_monomials_mod2(f_1_list, n)
	num_controls = 0
	for m in monomials:
		_, inds_1 = get_bit_inds(m,n)
		num_controls += len(inds_1)
	return num_controls
	
# ----------------------------------------------------------------------------------------	

# Brute Force Flips
#
# Description:
#	Given a function f (specified as in get_QROM_reduced_circuit above), search over the 
#	possible flips/negations of input bits to minimize the control point count of the QROM
#	circuit.
#
# Inputs:
#	f_1_list - the specification of the function f: a list of non-negative integers
#		between 0 and 2^n - 1, whose n-bit binary representation are the bit strings that
#		give f=1.
#
#	n - the number of input qubits
#
# Outputs:
#	k_best - the integer encoding of the optimal input bit flips
#	control_count_best - the optimal number of control points
#
# Requirements:
#	get_control_count from .

def brute_force_flips(f_1_list, n):
	
	# k encodes the possible flips of the input bits
	# k=0, no flips
	k_best = 0
	control_count_best = get_control_count(f_1_list, n)
	
	# k = 1, ..., 2^n-1: all other possible flips
	for k in range(1,2**n):
		f_1_list_flipped = [x^k for x in f_1_list]
		control_count = get_control_count(f_1_list_flipped, n)
		if control_count < control_count_best:
			k_best = k
			control_count_best = control_count
		
	return k_best, control_count_best