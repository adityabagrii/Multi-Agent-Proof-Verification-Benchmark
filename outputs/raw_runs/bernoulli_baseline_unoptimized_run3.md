Assumptions:
- $x \in \mathbb{R}, x \ge -1$
- $n \in \mathbb{Z}, n \ge 0$

Proof Strategy:
The proof proceeds by mathematical induction on $n$. The base case $n=0$ establishes the boundary condition. The inductive step utilizes the assumption $x \ge -1$ to ensure that multiplying by $(1+x)$ preserves the inequality direction, followed by the omission of a non-negative quadratic term to simplify to the target expression.

Numbered Proof Steps:
1.  **Base Case: $n = 0$**
    * **Claim:** $(1+x)^0 \ge 1 + (0)x$.
    * **Justification:** By the empty-product convention, $(1+x)^0 = 1$ for all $x \ge -1$ (including the $0^0$ case if $x=-1$). The right-hand side $1 + 0x = 1$. Since $1 \ge 1$, the base case holds.
2.  **Inductive Hypothesis**
    * **Claim:** Assume $(1+x)^k \ge 1 + kx$ for some integer $k \ge 0$.
    * **Justification:** Standard inductive assumption.
3.  **Inductive Step: Preparation**
    * **Claim:** $(1+x)^{k+1} = (1+x)^k(1+x)$.
    * **Justification:** Law of exponents for real numbers.
    * **Claim:** $1 + x \ge 0$.
    * **Justification:** Given assumption $x \ge -1$.
4.  **Application of Hypothesis**
    * **Claim:** $(1+x)^k(1+x) \ge (1+kx)(1+x)$.
    * **Justification:** Multiplication of both sides of the inductive hypothesis by the non-negative quantity $(1+x)$.
5.  **Expansion and Simplification**
    * **Claim:** $(1+kx)(1+x) = 1 + x + kx + kx^2 = 1 + (k+1)x + kx^2$.
    * **Justification:** Distributive property of real numbers (FOIL method).
6.  **Comparison and Transitivity**
    * **Claim:** $1 + (k+1)x + kx^2 \ge 1 + (k+1)x$.
    * **Justification:** Since $k \ge 0$ and $x^2 \ge 0$ for all real $x$, the term $kx^2$ is non-negative. Dropping a non-negative term from a sum results in a value less than or equal to the original sum.
    * **Claim:** $(1+x)^{k+1} \ge 1 + (k+1)x$.
    * **Justification:** Transitive property of inequality applied to steps 4, 5, and 6.

Equality Case:
* If $n=0$ or $n=1$, equality holds for all $x \ge -1$.
* If $x=0$, equality holds for all $n \ge 0$.
* For $n > 1$ and $x \neq 0$, the inequality is strict: $(1+x)^n > 1 + nx$.

Final Conclusion:
$(1+x)^n \ge 1 + nx$
