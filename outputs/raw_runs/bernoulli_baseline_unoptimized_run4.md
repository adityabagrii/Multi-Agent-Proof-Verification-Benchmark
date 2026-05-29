Assumptions:
- $x \ge -1$
- $n$ is a non-negative integer ($n \in \{0, 1, 2, \dots\}$)

Proof Strategy:
Mathematical induction on $n$. We establish the base case for $n=0$ and then prove that if the inequality holds for $k$, it must hold for $k+1$, utilizing the assumption $x \ge -1$ to ensure non-negative multipliers.

Numbered Proof Steps:
1.  **Base Case: $n = 0$.**
    * **Claim:** $(1+x)^0 \ge 1 + (0)x$.
    * **Justification:** By empty-product convention, $(1+x)^0 = 1$. The right side is $1 + 0 = 1$. Since $1 \ge 1$, the base case holds for all $x \ge -1$ (including $x=-1$).
2.  **Inductive Hypothesis.**
    * **Claim:** Assume $(1+x)^k \ge 1 + kx$ for some integer $k \ge 0$.
3.  **Inductive Step: $n = k + 1$.**
    * **Claim:** Multiply both sides of the hypothesis by $(1+x)$.
    * **Justification:** Since $x \ge -1$, it follows that $(1+x) \ge 0$. Multiplication by a non-negative quantity preserves inequality direction.
    * **Result:** $(1+x)^{k+1} \ge (1+kx)(1+x)$.
4.  **Algebraic Expansion.**
    * **Claim:** $(1+kx)(1+x) = 1 + x + kx + kx^2 = 1 + (k+1)x + kx^2$.
    * **Justification:** Distributive law of real numbers.
5.  **Lower Bound Comparison.**
    * **Claim:** $1 + (k+1)x + kx^2 \ge 1 + (k+1)x$.
    * **Justification:** Since $k \ge 0$ and $x^2 \ge 0$ for all real $x$, the term $kx^2$ is non-negative.
6.  **Transitivity.**
    * **Claim:** $(1+x)^{k+1} \ge 1 + (k+1)x$.
    * **Justification:** Transitive property of inequality applied to steps 3, 4, and 5.

Equality Case:
Equality holds when $n=0$, $n=1$, or $x=0$.

Final Conclusion:
$(1+x)^n \ge 1 + nx$
