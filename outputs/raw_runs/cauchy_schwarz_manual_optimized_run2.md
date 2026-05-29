Assumptions:
- $a_1, \dots, a_n$ and $b_1, \dots, b_n$ are real numbers.
- $n$ is a positive finite integer.

Proof Strategy:
The proof employs the non-negativity of a sum of squares. We define a quadratic function $P(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since $P(t) \ge 0$ for all real $t$, its discriminant must be non-positive, provided the quadratic coefficient is non-zero. The case where the quadratic coefficient is zero is handled separately as a boundary condition.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$**
    * **Claim:** If $\sum_{i=1}^n b_i^2 = 0$, the inequality holds.
    * **Justification:** Since $b_i^2 \ge 0$ for all $i$ in the real numbers, the sum being zero implies $b_i = 0$ for all $i = 1, \dots, n$. Substituting $b_i = 0$ into the left side: $(\sum a_i \cdot 0)^2 = 0$. Substituting into the right side: $(\sum a_i^2)(0) = 0$. Thus, $0 \le 0$ is satisfied.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$**
    * **Claim:** We can define a non-negative function $P(t) = \sum_{i=1}^n (a_i - t b_i)^2$.
    * **Justification:** For any real $t$, $(a_i - t b_i)^2 \ge 0$ by the property of squares of real numbers. The sum of non-negative terms is non-negative.
3.  **Expansion of the Quadratic**
    * **Claim:** $P(t) = (\sum_{i=1}^n b_i^2)t^2 - 2(\sum_{i=1}^n a_i b_i)t + (\sum_{i=1}^n a_i^2)$.
    * **Justification:** Expand the summand: $(a_i - t b_i)^2 = a_i^2 - 2 t a_i b_i + t^2 b_i^2$. Distribute the summation across terms and factor out constants relative to $i$.
4.  **Application of the Discriminant Condition**
    * **Claim:** The discriminant $\Delta$ of $P(t)$ satisfies $\Delta \le 0$.
    * **Justification:** Since $P(t) \ge 0$ for all real $t$ and the leading coefficient $A = \sum b_i^2$ is strictly positive (from Case 2), the quadratic polynomial has at most one real root. For a quadratic $At^2 + Bt + C$, this requires $B^2 - 4AC \le 0$.
5.  **Substitution of Coefficients**
    * **Claim:** $(-2\sum_{i=1}^n a_i b_i)^2 - 4(\sum_{i=1}^n b_i^2)(\sum_{i=1}^n a_i^2) \le 0$.
    * **Justification:** Substitute $A = \sum b_i^2$, $B = -2\sum a_i b_i$, and $C = \sum a_i^2$ into the discriminant formula.
6.  **Simplification to Target**
    * **Claim:** $4(\sum_{i=1}^n a_i b_i)^2 \le 4(\sum_{i=1}^n b_i^2)(\sum_{i=1}^n a_i^2)$.
    * **Justification:** Square the constant $(-2)^2 = 4$ and move the negative product to the right-hand side of the inequality.
7.  **Division by Constant**
    * **Claim:** $(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
    * **Justification:** Divide both sides by the positive constant 4; the inequality direction remains unchanged.

Equality Case:
Equality holds if and only if $P(t) = 0$ for some $t$. This occurs when $a_i = t b_i$ for all $i$ (the sequences are proportional) or if all $b_i = 0$.

Final Conclusion:
$$\left(\sum_{i=1}^n a_i b_i\right)^2 \le \left(\sum_{i=1}^n a_i^2\right)\left(\sum_{i=1}^n b_i^2\right)$$
