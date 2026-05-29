Assumptions:
- $x \in \mathbb{R}, x \ge -1$
- $n \in \mathbb{Z}, n \ge 0$

Proof Strategy:
Mathematical induction on $n$. We verify the base case $n=0$ and then use the assumption that $1+x \ge 0$ to ensure the inequality holds during the inductive step.

Numbered Proof Steps:
1.  **Base Case ($n = 0$):**
    * **Claim:** $(1+x)^0 \ge 1 + (0)x$.
    * **Justification:** By the empty-product convention, $(1+x)^0 = 1$ for all $x \ge -1$ (including $x = -1$). The right side is $1 + 0 = 1$. Since $1 \ge 1$, the base case holds.
2.  **Inductive Hypothesis:**
    * **Claim:** Assume $(1+x)^k \ge 1 + kx$ for some integer $k \ge 0$.
    * **Justification:** Standard premise for the principle of mathematical induction.
3.  **Inductive Step Setup:**
    * **Claim:** $(1+x)^{k+1} = (1+x)^k(1+x)$.
    * **Justification:** Definition of exponentiation for integers.
4.  **Applying Hypothesis and Sign Constraint:**
    * **Claim:** $(1+x)^k(1+x) \ge (1+kx)(1+x)$.
    * **Justification:** From assumptions, $x \ge -1 \implies 1+x \ge 0$. Multiplying both sides of the inductive hypothesis by a non-negative quantity preserves the inequality direction.
5.  **Algebraic Expansion:**
    * **Claim:** $(1+kx)(1+x) = 1 + x + kx + kx^2 = 1 + (k+1)x + kx^2$.
    * **Justification:** Distributive law of multiplication over addition.
6.  **Comparison to Target Expression:**
    * **Claim:** $1 + (k+1)x + kx^2 \ge 1 + (k+1)x$.
    * **Justification:** Since $k \ge 0$ and $x^2 \ge 0$ for all real $x$, the term $kx^2$ is non-negative. Dropping a non-negative term from a sum results in a value less than or equal to the original sum.
7.  **Transitivity:**
    * **Claim:** $(1+x)^{k+1} \ge 1 + (k+1)x$.
    * **Justification:** Transitive property of inequality applied to steps 4, 5, and 6.

Equality Case:
Equality holds when $n=0$, $n=1$, or $x=0$.

Final Conclusion:
$(1+x)^n \ge 1 + nx$
