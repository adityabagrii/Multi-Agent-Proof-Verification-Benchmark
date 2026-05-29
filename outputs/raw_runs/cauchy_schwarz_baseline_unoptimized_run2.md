Assumptions:
- $a_i, b_i \in \mathbb{R}$ for $i = 1, \dots, n$.
- $n$ is a positive finite integer.

Proof Strategy:
We define a quadratic function $P(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since $P(t) \geq 0$ for all real $t$, its discriminant must be non-positive. We treat the case where the leading coefficient is zero separately to avoid division by zero or a degenerate quadratic.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$.**
    Since $b_i$ are real, $\sum b_i^2 = 0$ implies $b_i = 0$ for all $i$. Substituting into the inequality:
    $( \sum a_i \cdot 0 )^2 \leq ( \sum a_i^2 )( 0 ) \implies 0 \leq 0$.
    The inequality holds.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$.**
    Define the function $P(t) = \sum_{i=1}^n (a_i - t b_i)^2$. By the property of squares, $P(t) \geq 0$ for all $t \in \mathbb{R}$.
3.  **Expand $P(t)$:**
    $P(t) = \sum_{i=1}^n (a_i^2 - 2t a_i b_i + t^2 b_i^2) = (\sum b_i^2)t^2 - 2(\sum a_i b_i)t + (\sum a_i^2)$.
4.  **Discriminant Analysis:**
    For a quadratic $At^2 + Bt + C \geq 0$ to hold for all $t$, the discriminant $\Delta = B^2 - 4AC$ must satisfy $\Delta \leq 0$.
    Here, $A = \sum b_i^2$, $B = -2\sum a_i b_i$, and $C = \sum a_i^2$.
5.  **Calculate $\Delta$:**
    $\Delta = (-2\sum a_i b_i)^2 - 4(\sum b_i^2)(\sum a_i^2) \leq 0$.
6.  **Simplify:**
    $4(\sum a_i b_i)^2 \leq 4(\sum a_i^2)(\sum b_i^2)$.
    Dividing by 4 yields $(\sum_{i=1}^n a_i b_i)^2 \leq (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.

Equality Case:
Equality holds if and only if $a_i = t b_i$ for all $i$ (the sequences are proportional), or if one sequence consists entirely of zeros.

Final Conclusion:
Therefore, for all real $a_i, b_i$, we have $(\sum_{i=1}^n a_i b_i)^2 \leq (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
