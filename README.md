#### 1. Quick overview of linear optics

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

$$ \ket{\psi_{out}} = \frac{1}{\sqrt{s_1! s_2! ... s_m!}} \prod_{i=1}^n \bigg(\sum_{j=1}^m u_{ji} a_j^{\dagger} \bigg)^{s_i} \ket{000...0}.$$ 

Developing the product gives a linear superposition of Fock states:

$$ \ket{\psi_{out}} = \frac{1}{\sqrt{s_1! s_2! ... s_m!}} \sum_{t \in \Phi_{m,n}} \alpha_t \sqrt{t_1!...t_m!} \ket{t_1,t_2,...,t_m}.$$ 

For more details about the formalism see [1]. 

**Perceval information** 

Given $U$ and an input state $\ket{s}$, Perceval can compute for you the coefficients $\alpha_t \sqrt{t_1!...t_m!}$ with two backends: 
- the Naive backend which gives you one specific coefficient for a chosen $\ket{t}$,
- the SLOS backend which gives you all coefficients. 

#### 2. Linear optical circuits 

The unitary operator applied can be itself described as a linear optical circuit made of constant beam splitters and parameterized phase shifters arranged in a fixed architecture also called a chip. A beam splitter (BS) applies the 2-mode unitary transformation 

$$ \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & i \\\ i & 1 \end{pmatrix} $$ 

and a phase shifter (PS) parameterized by an angle $\theta$ applies the 1-mode transformation 

$$ \begin{pmatrix} 1 & \\\ & e^{i\theta} \end{pmatrix}. $$

An example of circuit is given in Fig.1 with the corresponding unitary applied. 

<p align="center">
<img src="images/lo_circuit.png">
</p> 

Similarly to quantum circuits, the sequential composition is equivalent to matrix/matrix products. Where it differs is in the spatial composition where the direct sum is used.  Theoretical results guarantee that some chips are universal in the sense there always exists a set of angles of the beam splitters and phase shifters to implement any desired operator U [2,3].

**Perceval information**

Perceval can generate such universal chips for you and choose the angles to implement the unitary of your choice. You can also easily iterate through the angles of the circuits to choose yourself the unitary to apply. Then you can call Perceval's backends to perform some simulations .

#### 3. Probabilistic gates for NISQ 

For near-term applications, photonic hardware essentially relies on using a chip with an encoding to mimic the quantum circuit approach. For instance, in the dual rail encoding, one qubit is encoded as a photon that can be in two different spatial modes (thus encoding the $\ket{0}$ and $\ket{1}$ states) and the concatenation of $n$ photons with $2n$ modes gives an $n$-qubit quantum system. Note that at any moment each photon stays in its pair of modes.

<p align="center">
<img src="images/dual_rail.png">
</p> 

If one-qubit gates can be easily implemented by doing some local 2-mode operations (see Fig.2), unfortunately it is known that entangling 2-qubit gates cannot be implemented with the use of linear optics only. We need auxiliary modes and photons and some postselection schemes on the auxiliary modes to implement entangling gates [4]. Roughly, with auxiliary photons and modes, the output state is now a sum of a desired state (on which the correct 2-qubit gate has been applied) and a garbage state 

$$ \ket{\psi} = \alpha \ket{\psi_{desired}}\ket{s} + \sum_{s' \neq s} \beta \ket{\psi_{garbage, s'}} \ket{s'} $$

and we need to measure the register $\ket{s}$ to postselect on having measured $s$. This results in a probabilistic operation with probability of success $|\alpha|^2$ which prevents large quantum circuits to be executed because the probability of success decreases exponentially with the number of two-qubit gates. 

For instance, in the dual rail encoding, one can check that implementing a CZ gate between two qubits is equivalent to implementing a CZ gate between two modes, the modes encoding the state $\ket{1}$ of both qubits. A phase of (-1) is applied if we have one photon in each mode, i.e, 

$$ CZ \ket{s1,s2} = (-1)^{s1s2} \ket{s1, s2}, s1, s2 <= 1 $$ 

with **Fock state** notations. The constraints $s_1, s_2 \leq 1$ are ensured by the fact that we are in dual rail encoding such that only one photon can be found in one mode. 

So far, the best known scheme to do a CZ gate is Knill's version given in Fig.3 that has a probability of success of 2/27 [5]. It requires two extra photons, two extra modes and the gate is implemented if one photon is detected in each auxiliary mode.

<p align="center">
<img src="images/knill_cz.png">
</p> 

The matrix of the circuit is 

$$ U = \begin{pmatrix} -1/3 & -\sqrt{2}/3 & \sqrt{2}/3 & 2/3 \\\ \sqrt{2}/3 & -1/3 & -2/3 & \sqrt{2}/3 \\\ -\sqrt{3+\sqrt{6}}/3 & \sqrt{3 - \sqrt{6}}/3 & -\sqrt{(3+\sqrt{6})/2}/3 & \sqrt{1/6 - 1/(3\sqrt{6})} \\\ -\sqrt{3-\sqrt{6}}/3 & -\sqrt{3+\sqrt{6}}/3 & -\sqrt{1/6-1/(3\sqrt{6})} & -\sqrt{(3+\sqrt{6})/2}/3\end{pmatrix}.$$ 



One can check that for any input $\ket{s1,s2}$ on the first two modes, $s_1, s_2 \leq 1$, we get an output of the form 

$$ (-1)^{s_1s_2} \sqrt{\frac{2}{27}} \ket{s_1,s_2} \ket{1,1} + \alpha \ket{\star} \ket{0,0} + \beta \ket{\star} \ket{0,1} + \gamma \ket{\star}\ket{1,0} $$

and postselecting on the two auxiliary modes ensures we get the correct result.

#### 4. Goal of the challenge 

The goal of this challenge is to better understand the link between the linear optical circuit as a unitary on the modes and the resulting unitary operator on the Fock space and how we can design the search of more complex linear optical gates. To assess the quality of your work, we propose a $3$-mode linear optical gate to implement: the CCZ gate. At the qubit level, a CCZ gate applies the operation 

$$ CCZ \ket{x_1, x_2, x_3} = (-1)^{x_1x_2x_3} \ket{x_1, x_2, x_3} $$ 

and one can check that with a dual rail encoding this is equivalent, at the mode level, to the gate 

$$ CCZ \ket{s_1, s_2, s_3} = (-1)^{s_1s_2s_3} \ket{s_1, s_2, s_3},  s_1, s_2, s_3 \leq 1$$

where the modes $s_1, s_2, s_3$ are the ones encoding the state $\ket{1}$ of the three qubits.

Using standard circuit decomposition, the CCZ gate can be implemented as in Fig.4 with 6 CNOT gates but it is costly in terms of extra resources and success probability. You can still use it to check your code. 

In [6], they investigate the numerical search of a Toffoli gate, with promising results. However they do not provide a linear optical to check their result. You can start by trying to reproduce their results before improving on their work. 

<p align="center">
<img src="images/ccz.png">
</p> 

**Insights**

Both analytical and numerical work are promising leads. Feel free to choose the ones you prefer/feel is the more promising! Keep in mind that analytical work, if they do not end up with a practical result, will be harder to judge than numerical results. 

**Suggested guideline**

1. Start by reproducing the results from [5]. Do not necessary follow the exact same method. The goal is to have a code that can recover a CZ gate with success probability 2/27. 
2. Then reproduce the results from [6], either by applying your method from Question 1 or by designing a new method. 
3. More exploratory work is to find better implementations for both the Toffoli and the CCZ gate in hybrid encoding.
4. Any theoretical result is welcomed! Proofs that the current implementations are optimal with respect to any metrics (success probability, number of photons, etc.) are of particular interest.

Your mentors for this challenge will be Pierre-Emmanuel Emeriau and Samuel Horsch (on site) and Alexia Salavrakos and Timothé Goubalt (on Slack).

## 5. How to use Perceval to create a gate

### What is Perceval
Perceval is Quandela quantum simulation framework which **must** be used to solve any of these challenges

Perceval provides tools for composing circuits from linear optical components, defining single-photon sources, manipulating Fock states, running simulations, reproducing published experimental papers and experimenting with a new generation of quantum algorithms.

You can find documentation regarding Perceval here: https://perceval.quandela.net/docs/

And the source code repository is here: https://github.com/Quandela/Perceval

### Installation & Use
You have all the installation explanation on the github repository, we advise you to work on the version 0.10.3.

A lot of notebooks are available our github (in docs/source/notebooks) or in our documentation to inspire you.

If you have any issue, please contact either Marion Fabre (on site) or Eric Bertasi or Melvin Mathe (on Slack).

### What we expect
Create a GitHub repository, either add us (our usernames are in your github challenge repo) or send us the link (if it's public), and commit your code in this repository so we can keep track of your contribution. **Only** the code in the **main** branch will be reviewed and will be part of your evaluation.

The result of your work has to be a locally simulated [**Processor**](https://perceval.quandela.net/docs/reference/processor.html). The Processor class is a composition of a Perceval circuit with input states, ports and heralding function.

We **strongly** advise that you checkout the Perceval code and go read how we design our own gates in Perceval in perceval/components/core_catalog (or at least visit this github online [directory](https://github.com/Quandela/Perceval/tree/main/perceval/components/core_catalog) )

As your work will be autograded, the main branch of your git repository is required to follow this file architecture:
```
.
├── main.py
├── requirements.txt
├── README.md
```
- main.py should contain a method called "get_CCZ" with no argument that return a perceval Processor
- requirements.txt should contain all your scripts' python module dependencies, and follow the [requirements format](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
- README.md explains how to use your script and how you came up with this result(s)

Other files can be included in you git repository (like other python files, jupyter notebook, ...) but they will not be use by our autograder, nevertheless those files could be use to give you bonus point if you are selected as finalist.

### How the autograde works
Our autograder will rate 4 parameters, from the most to the less important:
- Fidelity
- Performance
- Number of Photon (ancillaries included)
- Number of Modes (heralds and ancillaries included)

#### Fidelity
Our Fidelity is the distance between your gate and the theoretical perfect one. It's calculating with the distance between probabilities.

#### Performance
This is a ratio of how many measurement we keep and how many measurement we throw away.

For instance, for Knill's CZ gate, the performance as stated above is 2/27.

#### Analyzer object
To get Fidelity and Performance, you can use the Analyzer. 

This object has been presented in the remote Perceval workshop with the notebook "Getting started with Perceval".

Since the Analyzer can only inspect logical space, you can change your CZ or CCZ gate to CNOT or CCNOT (Toffoli) by adding Hadamard gates around the data qubit:
``` python
import perceval as pcvl

processor = pcvl.Processor("SLOS", 4)
processor.add(2, pcvl.BS.H())
processor.add(0, pcvl.catalog["heralded cz"].build_processor())
processor.add(2, pcvl.BS.H())

states = {
    pcvl.BasicState([1, 0, 1, 0]): "00",
    pcvl.BasicState([1, 0, 0, 1]): "01",
    pcvl.BasicState([0, 1, 1, 0]): "10",
    pcvl.BasicState([0, 1, 0, 1]): "11"
}

ca = pcvl.algorithm.Analyzer(processor, states)

truth_table = {"00": "00", "01": "01", "10": "11", "11": "10"}
ca.compute(expected=truth_table)

pcvl.pdisplay(ca)
print(
    f"performance = {ca.performance}, fidelity = {ca.fidelity.real}")
```
Output:
```bash
    00	01	10	11
00	1	0	0	0
01	0	1	0	0
10	0	0	0	1
11	0	0	1	0
performance = 0.074066, fidelity = 0.9999999915267557
```

### Bonus 

If you think you have successfully answered the challenge above but that sleeping is cheating, we have an extra challenging question for you. It's a bit more tricky than the first one so you shouldn't address this if you have not completed the first challenge. 

This challenge is about a special CZ gate in an __hybrid__ qubit encoding. We slightly deviate from the dual rail encoding. Two qubits are encoded in one photon and 4 modes and a third qubit is encoded as one photon with 2 modes. We want to apply a CZ gate between one of the first two qubits and the third qubit. Without loss of generality, let's assume we want to do CNOT(2,3). At the Fock state level, given the modes that encode the states $\ket{01}$ and $\ket{11}$ of the first two qubits (resp. $s_1$ and $s_2$) and the third mode that encodes the state $\ket{1}$ of the third qubit ($s_3$), we want to do the operation 

$$ \ket{s_1,s_2,s_3} \to (-1)^{(s_1 + s_2)s_3} \ket{s_1,s_2,s_3}. $$

This operation can be rewritten as 

$$ \ket{s_1,s_2,s_3} \to (-1)^{s_1s_3} (-1)^{s_2s_3} \ket{s_1,s_2,s_3} $$

which is equivalent to applying two CZ gates. Can we do better with a direct implementation? 

Fig.5 and Fig.6 gives a recap of the two gates we are looking for in a Fock state formalism.

<p align="center">
<img src="images/toffoli.png">
</p> 

<p align="center">
<img src="images/special_cz.png">
</p> 

Note that the behavior of the gates is not defined for larger number of photons. We do not care as these cases will never happen if we stay in the chosen encoding.

Good luck!

#### References 

[1] Aaronson, S., & Arkhipov, A. (2011, June). The computational complexity of linear optics. In Proceedings of the forty-third annual ACM symposium on Theory of computing (pp. 333-342).

[2] Reck, M., Zeilinger, A., Bernstein, H. J., & Bertani, P. (1994). Experimental realization of any discrete unitary operator. Physical review letters, 73(1), 58.

[3] Clements, W. R., Humphreys, P. C., Metcalf, B. J., Kolthammer, W. S., & Walmsley, I. A. (2016). Optimal design for universal multiport interferometers. Optica, 3(12), 1460-1465.

[4] Knill, E., Laflamme, R., & Milburn, G. J. (2001). A scheme for efficient quantum computation with linear optics. nature, 409(6816), 46-52.

[5] Knill, E. (2002). Quantum gates using linear optics and postselection. Physical Review A, 66(5), 052306.

[6] Uskov, D. B., Kaplan, L., Smith, A. M., Huver, S. D., & Dowling, J. P. (2009). Maximal success probabilities of linear-optical quantum gates. Physical Review A, 79(4), 042326.


```python

```
