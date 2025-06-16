# SELECT QROM via Polynomial Reduction
This repository implements a SELECT-style Quantum ROM for boolean functions in Qiskit that aims to improve on circuit complexity over the naive SELECT implementation without using ancillae. Provided a boolean function $f: \mathbb{F}_2^n \rightarrow \mathbb{F}_2$ that maps length-$`n`$ bit strings $`x_{n-1} x_{n-2}\ldots x_1 x_0`$ to an output bit, this code first represents the function as a polynomial on $x_0, x_1, \ldots$, simplifies that polynomial, and then generates a circuit $U$ that, like the naive SELECT circuit, has the action

$$U \left|x\right>_n \left|y\right>_1 = \left|x\right>_n \left|y \oplus f(x)\right>_1.$$

The resulting circuit, as compared with the naive implementation, will typically use fewer multi-controlled $X$ gates and/or use multi-controlled $X$ gates with fewer control qubits. Specifically, included in this code is an optimization procedure that minimizes the number total number of control qubits across all multi-controlled X gates. Given that multi-controlled X gates can be implemented with circuit depth linear in the number of controls ([Saeedi and Pedram 2013](http://arxiv.org/abs/1303.3557)), this heuristic roughly optimizes for depth of the circuit (while using no ancillae).

### Motivating Example

As an example, consider the function $f$ on length $4$ bit strings that maps $0001$, $0011$, and $0101$ to $1$ and all other bit strings to $0$. The naive SELECT QROM makes use of the fact that $f$ can be represented by the following boolean polynomial:

$$f(x_3 x_2 x_1 x_0) = p_{\mathrm{bool}}(x_0, x_1, x_2, x_3) = x_0 \land \overline{x_1} \land \overline{x_2} \land \overline{x_3} \oplus x_0 \land x_1 \land \overline{x_2} \land \overline{x_3}  \oplus x_0 \land \overline{x_1} \land x_2 \land \overline{x_3}.$$

Since this polynomial contains three terms with four factors each, the naive implementation requires three multi-controlled $X$ gates each with four control qubits, i.e. three $C^4X$ gates, and a number of $X$ gates to implement the negations:

![naive](https://github.com/user-attachments/assets/e04359ac-dd67-419a-b299-ea771710c473)

Following ([Mukhopadhyay 2025](https://www.nature.com/articles/s41598-025-95283-5)), we note that, interpreting the $x_k$ and $f$ as the numbers $0$ or $1$ instead of logical bits, the above polynomial is equivalent to

$$f(x_3 x_2 x_1 x_0) \equiv p(x_0, x_1, x_2, x_3) = x_0 (1+x_1) (1+x_2) (1+x_3) + x_0 x_1 (1+x_2) (1+x_3) + x_0 (1+x_1) x_2 (1+x_3) \\;(\mathrm{mod} 2),$$

which can be simplified to 

$$p(x_0, x_1, x_2, x_3) = x_0 (1+x_3) + x_0 x_1 x_2 (1+x_3) \\;(\mathrm{mod} 2).$$

Equivalently, in boolean form,

$$p_{\mathrm{bool}}(x_0, x_1, x_2, x_3) = x_0 \land \overline{x_3}  \oplus x_0 \land x_1 \land x_2 \land \overline{x_3},$$

which can be implemented with only two $X$ gates, a $C^2X$, and a $C^4X$ gate:

![poly_optimized](https://github.com/user-attachments/assets/b224ff40-d201-4011-9095-cfb5455138e6)


This circuit has $6$ total control points, as compared with $12$ for the naive circuit, and so has a depth that is roughly half.

### Implementation Details

For more implementation details and a thorough comparison with the naive implementation, see the iPython notebook in this repository. For a basic usage example, see below.

### Usage Example



