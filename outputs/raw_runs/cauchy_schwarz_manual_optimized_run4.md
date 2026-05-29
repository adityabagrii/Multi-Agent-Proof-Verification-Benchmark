Assumptions:
- $a_1, \dots, a_n$ and $b_1, \dots, b_n$ are real numbers.
- $n$ is a positive finite integer.

Proof Strategy:
Handle the case where the sum of squares of $b_i$ is zero separately. For the non-zero case, define a non-negative quadratic function $P(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Use the property that its discriminant must be non-positive to derive the inequality.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$.**
    * **Claim:** If $\sum_{i=1}^n b_i^2 = 0$, then $b_i = 0$ for all $i \in \{1, \dots, n\}$.
    * **Justification:** Property of real numbers: a sum of squares of real numbers is zero if and only if each term is zero.
    * **Claim:** The inequality holds as $0 \le 0$.
    * **Justification:** If $b_i = 0$, then $\sum a_i b_i = 0$ and $\sum b_i^2 = 0$. Both sides of the inequality $(\sum a_i b_i)^2 \le (\sum a_i^2)(\sum b_i^2)$ evaluate to $0$.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$.**
    * **Claim:** Define $P(t) = \sum_{i=1}^n (a_i - t b_i)^2 \ge 0$ for any $t \in \mathbb{R}$.
    * **Justification:** Squares of real numbers are non-negative, and the sum of non-negative numbers is non-negative.
3.  **Expansion of the Quadratic.**
    * **Claim:** $P(t) = (\sum b_i^2)t^2 - 2(\sum a_i b_i)t + (\sum a_i^2) \ge 0$.
    * **Justification:** Linearity of summation and the algebraic expansion $(a_i - t b_i)^2 = a_i^2 - 2t a_i b_i + t^2 b_i^2$.
4.  **Discriminant Condition.**
    * **Claim:** For a quadratic $At^2 + Bt + C \ge 0$ with $A > 0$ to hold for all $t$, the discriminant $\Delta = B^2 - 4AC$ must satisfy $\Delta \le 0$.
    * **Justification:** Quadratic formula and the requirement that the parabola has at most one real root (it does not cross below the t-axis).
5.  **Application of the Discriminant.**
    * **Claim:** $(-2 \sum a_i b_i)^2 - 4(\sum b_i^2)(\sum a_i^2) \le 0$.
    * **Justification:** Substitution of $A = \sum b_i^2$, $B = -2 \sum a_i b_i$, and $C = \sum a_i^2$ into the discriminant formula.
6.  **Simplification to Final Form.**
    * **Claim:** $4(\sum a_i b_i)^2 \le 4(\sum a_i^2)(\sum b_i^2)$.
    * **Justification:** Algebra (moving the negative term to the right side).
    * **Claim:** $(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
    * **Justification:** Division by the positive constant 4.

Equality Case:
Equality holds if and only if there exists a $t$ such that $a_i = t b_i$ for all $i$ (the vectors are linearly dependent), or if all $a_i=0$ or $b_i=0$.

Final Conclusion:
$(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$
