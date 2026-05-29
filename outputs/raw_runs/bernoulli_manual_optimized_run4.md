Assumptions:
- $x \geq -1$
- $n$ is a nonnegative integer ($n \in \{0, 1, 2, \dots\}$)

Proof Strategy:
We will use **Mathematical Induction** on the variable $n$. We will establish the base case for $n=0$ and then use the inductive hypothesis to show that if the inequality holds for $k$, it must hold for $k+1$, leveraging the fact that $(1+x)$ is non-negative to preserve inequality direction during multiplication.

Numbered Proof Steps:
1.  **Base Case ($n = 0$):**
    * **Claim:** $(1+x)^0 \geq 1 + (0)x$.
    * **Justification:** By the empty-product convention, $(1+x)^0 = 1$ for all $x$, including the boundary case $x = -1$ where $0^0 = 1$. The right-hand side simplifies to $1 + 0 = 1$. Since $1 \geq 1$, the base case holds.
2.  **Inductive Hypothesis:**
    * **Claim:** Assume $(1+x)^k \geq 1 + kx$ for some integer $k \geq 0$.
    * **Justification:** Standard assumption for the inductive step in a proof by induction.
3.  **Establish Positivity of Multiplier:**
    * **Claim:** $(1+x) \geq 0$.
    * **Justification:** Derived from the initial assumption $x \geq -1$ by adding $1$ to both sides.
4.  **Inductive Multiplication:**
    * **Claim:** $(1+x)^k(1+x) \geq (1+kx)(1+x)$.
    * **Justification:** Multiplication Property of Inequality. Since $(1+x) \geq 0$ (Step 3), multiplying both sides of the inductive hypothesis (Step 2) by $(1+x)$ preserves the inequality direction.
5.  **Simplify Left-Hand Side:**
    * **Claim:** $(1+x)^{k+1} \geq (1+kx)(1+x)$.
    * **Justification:** Product of powers rule: $a^k \cdot a^1 = a^{k+1}$.
6.  **Expand Right-Hand Side:**
    * **Claim:** $(1+x)^{k+1} \geq 1 + x + kx + kx^2$.
    * **Justification:** Distributive property (FOIL method) applied to $(1+kx)(1+x)$.
7.  **Factor Linear Terms:**
    * **Claim:** $(1+x)^{k+1} \geq 1 + (k+1)x + kx^2$.
    * **Justification:** Factoring the common term $x$ from the middle terms.
8.  **Analyze Quadratic Term:**
    * **Claim:** $kx^2 \geq 0$.
    * **Justification:** Since $k \geq 0$ (assumption) and $x^2 \geq 0$ for any real $x$ (Trivial Inequality), their product must be non-negative.
9.  **Transitive Inequality Comparison:**
    * **Claim:** $1 + (k+1)x + kx^2 \geq 1 + (k+1)x$.
    * **Justification:** Addition Property of Inequality; adding a non-negative value ($kx^2$) to $1 + (k+1)x$ results in a value greater than or equal to the original expression.
10. **Conclusion of Inductive Step:**
    * **Claim:** $(1+x)^{k+1} \geq 1 + (k+1)x$.
    * **Justification:** Transitive property of inequality applied to Step 7 and Step 9.

Equality Case:
Equality holds when $n=0$, $n=1$, or $x=0$. For $n>1$ and $x\neq 0$, the inequality is strict.

Final Conclusion:
By the principle of mathematical induction, for $x \geq -1$ and integer $n \geq 0$:
$$(1+x)^n \geq 1 + nx$$
