## SELECT QROM via Polynomial Reduction
This repository implements in Qiskit a SELECT-style Quantum ROM for boolean functions that aims to improve on circuit complexity over the naive SELECT implementation. Provided a boolean function $f: \mathbb{F}_2^n \rightarrow \mathbb{F}_2$ that maps length-$`n`$ bit strings $`x_{n-1} x_{n-2}\ldots x_1 x_0`$ to an output bit, this code first represents the function as a polynomial on $x_0, x_1, \ldots$, simplifies that polynomial, and then generates a circuit $U$ that, like the naive SELECT circuit, has the action

$$U \left|x\right>_n \left|y\right>_1 = \left|x\right>_n \left|y \oplus f(x)\right>_1$$

and uses no ancillae. The resulting circuit, as compared with the naive implementation, will typically use fewer multi-controlled $X$ gates and/or uses multi-controlled $X$ gates with fewer control qubits. Specifically, included in this code is an optimization procedure that attempts to minimze the total number of control qubits across all multi-controlled $X$ gates. Given that multi-controlled $X$ gates can be implemented with circuit depth linear in the number of controls ([Saeedi and Pedram 2013](http://arxiv.org/abs/1303.3557)), this heuristic roughly optimizes for depth of the circuit while using no ancillae.

### Implementation Details

For implementation details, a thorough comparison with the naive implementation, and a discussion of limitations and future steps, see [the iPython notebook](https://github.com/avijka/SELECT_QROM_polynomial-reduction/blob/main/SELECT_QROM_polynomial-reduction.ipynb) in this repository. For a basic usage example, see below.

### Usage Example
The main function is `get_QROM_reduced_circuit`, which, at minimum, takes in a list of integers (which represents the function $f$) and the number of input qubits $n$. The list contains elements of $`\{0,1,\ldots 2^n -1\}`$, whose binary representations match those bit string inputs for which $f=1$. For example, if $f(0001)=1$, $f(0011)=1$, and $f(0101)=1$, and all other inputs give $0$, pass the list `[1,3,5]` to `get_QROM_reduced_circuit`:

```python
from resources.QROM_polynomial_reduction import get_QROM_reduced_circuit

n = 4
inputs_f_eq_1 = [1,3,5]

qc = get_QROM_reduced_circuit(inputs_f_eq_1, n)
qc.draw(output="mpl", style="bw")
```

This will produce the following circuit:

![poly_optimized](https://github.com/user-attachments/assets/50e56fef-f218-499d-85ca-d51d80bdb51f)

This is a significant improvement over the naive SELECT implementation, which produces the following circuit:

![naive](https://github.com/user-attachments/assets/ff81dac4-f293-45c7-a191-b4144ebbc574)
