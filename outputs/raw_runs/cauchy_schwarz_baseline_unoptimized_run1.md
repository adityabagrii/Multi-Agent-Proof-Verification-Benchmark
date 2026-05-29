Assumptions:
- $a_i, b_i \in \mathbb{R}$ for $i = 1, \dots, n$
- $n \in \mathbb{Z}^+$

Proof Strategy:
Consider the non-negativity of a sum of squares. Handle the case where the norm of $b$ is zero separately to avoid division by zero, then use a quadratic polynomial in $t$ to derive the inequality via the discriminant or optimal parameter selection.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$.**
    Since $b_i$ are real, this implies $b_i = 0$ for all $i$. Substituting into the inequality:
    $( \sum a_i \cdot 0 )^2 \leq ( \sum a_i^2 )( \sum 0^2 ) \implies 0 \leq 0$.
    The inequality holds.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$.**
    Define a function $f(t)$ for $t \in \mathbb{R}$:
    $$f(t) = \sum_{i=1}^n (a_i - t b_i)^2$$
    Since $f(t)$ is a sum of squares, $f(t) \geq 0$ for all $t$.
3.  **Expand the quadratic:**
    $$f(t) = \sum_{i=1}^n (a_i^2 - 2t a_i b_i + t^2 b_i^2) = \left( \sum a_i^2 \right) - 2t \left( \sum a_i b_i \right) + t^2 \left( \sum b_i^2 \right)$$
4.  **Set the parameter $t$:**
    Let $A = \sum a_i^2$, $B = \sum a_i b_i$, and $C = \sum b_i^2$. Since $C > 0$, we can choose $t = \frac{B}{C}$. Substitute $t$ into $f(t) \geq 0$:
    $$A - 2\left(\frac{B}{C}\right)B + \left(\frac{B}{C}\right)^2 C \geq 0$$
    $$A - \frac{2B^2}{C} + \frac{B^2}{C} \geq 0 \implies A - \frac{B^2}{C} \geq 0$$
5.  **Rearrangement:**
    Multiply by $C$ (where $C > 0$):
    $$AC \geq B^2 \implies \left( \sum_{i=1}^n a_i^2 \right) \left( \sum_{i=1}^n b_i^2 \right) \geq \left( \sum_{i=1}^n a_i b_i \right)^2$$

Equality Case:
Equality holds if and only if $a_i - t b_i = 0$ for all $i$, meaning the sequences $(a_i)$ and $(b_i)$ are linearly dependent (proportional).

Final Conclusion:
For all $a_i, b_i \in \mathbb{R}$, $(\sum_{i=1}^n a_i b_i)^2 \leq (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
