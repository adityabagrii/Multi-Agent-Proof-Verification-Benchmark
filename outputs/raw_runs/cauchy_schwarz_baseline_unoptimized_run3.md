Assumptions:
- $a_i, b_i \in \mathbb{R}$ for $i = 1, \dots, n$.
- $n$ is a positive finite integer.

Proof Strategy:
We utilize the non-negativity of a sum of squares. We first handle the trivial case where the right-hand side is zero to avoid division by zero, then analyze a quadratic polynomial in $t$ and use its discriminant properties.

Numbered Proof Steps:
1.  **Base Case:** Suppose $\sum_{i=1}^n b_i^2 = 0$. Since $b_i$ are real, this implies $b_i = 0$ for all $i$. Consequently, $\sum a_i b_i = 0$. Both sides of the inequality become $0 \le 0$, which is true.
2.  **General Case:** Assume $\sum_{i=1}^n b_i^2 > 0$. For any $t \in \mathbb{R}$, consider the function:
    $$f(t) = \sum_{i=1}^n (a_i - t b_i)^2$$
3.  **Non-negativity:** Since $f(t)$ is a sum of squares, $f(t) \ge 0$ for all $t$. Expanding the expression:
    $$f(t) = \sum_{i=1}^n (a_i^2 - 2t a_i b_i + t^2 b_i^2) = \left(\sum a_i^2\right) - 2t\left(\sum a_i b_i\right) + t^2\left(\sum b_i^2\right) \ge 0$$
4.  **Discriminant Argument:** Let $A = \sum a_i^2$, $B = \sum a_i b_i$, and $C = \sum b_i^2$. The quadratic $Ct^2 - 2Bt + A \ge 0$ holds for all $t$. For a quadratic with a positive leading coefficient $C$ to be non-negative for all $t$, its discriminant $\Delta$ must be non-positive:
    $$\Delta = (-2B)^2 - 4(C)(A) \le 0$$
5.  **Simplification:**
    $$4B^2 - 4AC \le 0 \implies B^2 \le AC$$
    Substituting back the sums:
    $$\left(\sum_{i=1}^n a_i b_i\right)^2 \le \left(\sum_{i=1}^n a_i^2\right) \left(\sum_{i=1}^n b_i^2\right)$$

Equality Case:
Equality holds if and only if $a_i = t b_i$ or $b_i = t a_i$ for some constant $t$ (i.e., the sequences are linearly dependent).

Final Conclusion:
Therefore, for all $a_i, b_i \in \mathbb{R}$, $\left(\sum_{i=1}^n a_i b_i\right)^2 \le \left(\sum_{i=1}^n a_i^2\right)\left(\sum_{i=1}^n b_i^2\right)$.
