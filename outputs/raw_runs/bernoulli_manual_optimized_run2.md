Assumptions:
- $x \in \mathbb{R}$ such that $x \geq -1$.
- $n$ is a nonnegative integer ($n \in \{0, 1, 2, \dots\}$).

Proof Strategy:
We will use mathematical induction on the variable $n$. We will first establish the base case for $n=0$ and then prove that if the inequality holds for an arbitrary $n=k$, it must also hold for $n=k+1$.

Numbered Proof Steps:
1.  **Base Case ($n=0$):**
    * **Claim:** $(1+x)^0 \geq 1 + (0)x$.
    * **Justification:** By the empty-product convention, $(1+x)^0 = 1$ for all $x \geq -1$, including the case $x=-1$ (where $0^0$ is treated as $1$ in this context). Since $1 + 0x = 1$, the statement simplifies to $1 \geq 1$, which is true.
2.  **Inductive Hypothesis:**
    * **Claim:** Assume $(1+x)^k \geq 1 + kx$ for some integer $k \geq 0$.
    * **Justification:** Standard inductive assumption for mathematical induction.
3.  **Inductive Step Preparation (Sign Check):**
    * **Claim:** $1+x \geq 0$.
    * **Justification:** Given assumption $x \geq -1$.
4.  **Multiplying by $(1+x)$:**
    * **Claim:** $(1+x)^k(1+x) \geq (1+kx)(1+x)$.
    * **Justification:** Multiplication of both sides of the Inductive Hypothesis by a non-negative quantity ($(1+x) \geq 0$) preserves the direction of the inequality.
5.  **Expansion of the Right-Hand Side:**
    * **Claim:** $(1+x)^{k+1} \geq (1+kx)(1+x)$.
    * **Justification:** The left side of Step 4 is $(1+x)^k(1+x)=(1+x)^{k+1}$ by the product rule for nonnegative integer exponents.
6.  **Factoring the Right-Hand Side:**
    * **Claim:** $(1+kx)(1+x)=1+x+kx+kx^2=1+(k+1)x+kx^2$.
    * **Justification:** Distributive law of multiplication over addition, followed by collecting $x+kx=(k+1)x$.
7.  **Analysis of the Quadratic Term:**
    * **Claim:** $kx^2 \geq 0$.
    * **Justification:** Since $k \geq 0$ (assumption) and $x^2 \geq 0$ (square of a real number is non-negative), their product is non-negative.
8.  **Simplification via Transitivity:**
    * **Claim:** $(1+x)^{k+1} \geq 1 + (k+1)x + kx^2 \geq 1 + (k+1)x$.
    * **Justification:** Steps 5 and 6 give the first inequality. Step 7 shows $kx^2$ is non-negative, so removing it gives a lower bound.
9.  **Conclusion of Inductive Step:**
    * **Claim:** $(1+x)^{k+1} \geq 1 + (k+1)x$.
    * **Justification:** Transitive property of inequality applied to step 8.

Equality Case:
Equality holds when $n=0$, $n=1$, or $x=0$. For $n>1$ and $x\neq 0$, the inequality is strict.

Final Conclusion:
By the principle of mathematical induction, for $x \geq -1$ and integer $n \geq 0$:
$$(1+x)^n \geq 1 + nx$$
