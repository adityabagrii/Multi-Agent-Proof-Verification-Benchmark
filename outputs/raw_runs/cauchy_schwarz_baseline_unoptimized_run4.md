Assumptions:
- $a_i, b_i \in \mathbb{R}$ for all $i \in \{1, \dots, n\}$.
- $n$ is a positive finite integer.

Proof Strategy:
The proof utilizes the non-negativity of a sum of squares. We define a quadratic function in terms of a real parameter $t$. By analyzing the discriminant of this quadratic (after handling the case where the leading coefficient is zero), we establish the inequality.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$.**
    Since each $b_i$ is a real number, $b_i^2 \geq 0$. Thus, $\sum_{i=1}^n b_i^2 = 0$ implies $b_i = 0$ for all $i$. In this case, both sides of the inequality evaluate to $0$, satisfying $0 \leq 0$.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$.**
    Consider the function $f(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since $f(t)$ is a sum of squares, $f(t) \geq 0$ for all $t \in \mathbb{R}$.
3.  **Expansion of the Quadratic:**
    Expanding the terms gives:
    $$f(t) = \sum_{i=1}^n (a_i^2 - 2t a_i b_i + t^2 b_i^2) = \left( \sum_{i=1}^n b_i^2 \right) t^2 - 2 \left( \sum_{i=1}^n a_i b_i \right) t + \left( \sum_{i=1}^n a_i^2 \right)$$
4.  **Discriminant Analysis:**
    Since $f(t) \geq 0$ for all $t$, the quadratic $At^2 + Bt + C$ has at most one real root. Therefore, its discriminant $\Delta = B^2 - 4AC$ must be non-positive:
    $$\Delta = \left[ -2 \left( \sum_{i=1}^n a_i b_i \right) \right]^2 - 4 \left( \sum_{i=1}^n b_i^2 \right) \left( \sum_{i=1}^n a_i^2 \right) \leq 0$$
5.  **Simplification:**
    $$4 \left( \sum_{i=1}^n a_i b_i \right)^2 \leq 4 \left( \sum_{i=1}^n b_i^2 \right) \left( \sum_{i=1}^n a_i^2 \right)$$
    Dividing by 4 yields the desired result.

Equality Case:
Equality holds if and only if $a_i - t b_i = 0$ for all $i$, meaning the sequences $(a_i)$ and $(b_i)$ are proportional (i.e., there exists some scalar $t$ such that $a_i = t b_i$ or $b_i = 0$).

Final Conclusion:
For all $a_i, b_i \in \mathbb{R}$, $(\sum_{i=1}^n a_i b_i)^2 \leq (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
