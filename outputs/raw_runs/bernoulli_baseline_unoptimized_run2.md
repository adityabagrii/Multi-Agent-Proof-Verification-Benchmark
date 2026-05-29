Assumptions:
- $x \ge -1$
- $n$ is a nonnegative integer ($n \in \{0, 1, 2, \dots\}$)

Proof Strategy:
Mathematical induction on $n$. The base case $n=0$ is verified first. The inductive step uses the assumption $x \ge -1$ to ensure that multiplying by $(1+x)$ preserves the inequality.

Numbered Proof Steps:
1.  **Base Case: $n = 0$.**
    * **Claim:** $(1+x)^0 \ge 1 + (0)x$.
    * **Justification:** By the empty-product convention, $(1+x)^0 = 1$ for all $x \ge -1$ (including $x = -1$). The right side $1 + 0 = 1$. Since $1 \ge 1$, the base case holds.
2.  **Inductive Hypothesis.**
    * **Claim:** Assume $(1+x)^k \ge 1 + kx$ for some integer $k \ge 0$.
    * **Justification:** Standard inductive assumption.
3.  **Inductive Step Setup.**
    * **Claim:** Multiply both sides of the hypothesis by $(1+x)$.
    * **Justification:** Since $x \ge -1$, it follows that $1+x \ge 0$. Multiplying an inequality by a non-negative quantity preserves the inequality sign.
4.  **Algebraic Expansion.**
    * **Claim:** $(1+x)^{k+1} \ge (1+kx)(1+x) = 1 + x + kx + kx^2$.
    * **Justification:** Distributive property of real numbers.
5.  **Simplification and Inequality Chain.**
    * **Claim:** $1 + (k+1)x + kx^2 \ge 1 + (k+1)x$.
    * **Justification:** Since $k \ge 0$ and $x^2 \ge 0$, the term $kx^2$ is non-negative. Dropping a non-negative term from the sum results in a value less than or equal to the original.
6.  **Inductive Conclusion.**
    * **Claim:** $(1+x)^{k+1} \ge 1 + (k+1)x$.
    * **Justification:** Transitive property of inequalities applied to steps 4 and 5.

Equality Case:
Equality holds when $n=0$, $n=1$, or $x=0$. If $n > 1$ and $x > -1$, equality holds only if $x=0$.

Final Conclusion:
$(1+x)^n \ge 1 + nx$
