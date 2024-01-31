# Quandela iQuHACK 2024 Remote Challenge


## 1. Quick overview of linear optics

Linear optics describe the evolution of photons passing through a linear interferometer. Given a circuit with $m$ modes and $n$ photons, we use the Fock state notation 
$$\ket{s_1,s_2, ..., s_m}, s_1+s_2+...+s_m = n$$ 

to represent a state with $s_1$ photons in mode $1$, up to $s_m$ photons in mode $m$ and we note $\Phi_{m,n}$ the set of possible $n$-photon $m$-mode Fock states.

Equivalently, a Fock state can be written as the result of creation operators $a^{\dagger}$ on each mode applied to the vacuum state. The generic formula is 

$$ a^{\dagger}\ket{n} = \sqrt{n+1} \ket{n+1}$$ 

such that 

$$\ket{s_1, s_2, ..., s_m}= \frac{1}{\sqrt{s_1! s_2! ... s_m!}} (a_1^{\dagger})^{s_1} (a_2^{\dagger})^{s_2} ... (a_m^{\dagger})^{s_m} \ket{000...0}.$$ 

When the photons pass through a linear interferometer, the evolution is modeled as applying unitary linear transformations to the creation operators. In other words, there exists a unitary operator U that applies the transformations 

$$ a_i^{\dagger} \to \sum_{j=1}^m u_{ji} a_j^{\dagger} $$  

and the output state is given by 

$$ \ket{\psi_{out}} = \frac{1}{\sqrt{s_1! s_2! ... s_m!}} \prod_{i=1}^n \bigg(\sum_{j=1}^m u_{ji} a_j^\dagger \bigg)^{s_i} \ket{000...0}.$$ 

Developping the product gives a linear superposition of Fock states:

$$ \ket{\psi_{out}} = \frac{1}{\sqrt{s_1! s_2! ... s_m!}} \sum_{t \in \Phi_{m,n}} \alpha_t \sqrt{t_1!...t_m!} \ket{t_1,t_2,...,t_m}.$$ 

For more details about the formalism see [1]. 

**Perceval information** 

Given $U$ and an input state $\ket{s}$, Perceval can compute for you the coefficients $\alpha_t \sqrt{t_1!...t_m!}$ with two backends: 
- the Naive backend which gives you one specific coefficient for a chosen $\ket{t}$,
- the SLOS backend which gives you all coefficients.

## 2. Linear optical circuits 

The unitary operator applied can be itself described as a linear optical circuit made of constant beam splitters and parameterized phase shifters arranged in a fixed architecture also called a chip. A beam splitter applies the 2-mode unitary transformation 

$$ \begin{pmatrix} 1 & i \\\ i & 1 \end{pmatrix} $$ 

and a phase shifter parameterized by an angle $\theta$ applies the 1-mode transformation 

$$ \begin{pmatrix} 1 & \\\ & e^{i\theta} \end{pmatrix}. $$

An example of circuit is given in Fig.1 with the corresponding unitary applied. 
