Assumptions:
- $a_1, \dots, a_n$ and $b_1, \dots, b_n$ are real numbers.
- $n$ is a positive finite integer.

Proof Strategy:
The proof employs a quadratic polynomial argument. We first address the case where the sum of squares of $b_i$ is zero to avoid division by zero. For the non-zero case, we construct a non-negative quadratic function $f(t) = \sum (a_i - t b_i)^2$ and analyze its discriminant. Since the quadratic is always non-negative, its discriminant must be less than or equal to zero, which directly yields the Cauchy-Schwarz inequality.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$**
    * **Claim:** If $\sum_{i=1}^n b_i^2 = 0$, then the inequality holds as an equality.
    * **Justification:** For real numbers, a sum of squares is zero if and only if each term is zero. Thus, $b_i = 0$ for all $i \in \{1, \dots, n\}$.
    * **Calculation:**
        * Left-hand side (LHS): $(\sum a_i \cdot 0)^2 = 0^2 = 0$.
        * Right-hand side (RHS): $(\sum a_i^2)(0) = 0$.
    * **Result:** $0 \le 0$, which is true.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$**
    * **Claim:** We can define a quadratic function $f(t)$ that is non-negative for all real $t$.
    * **Justification:** Let $f(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since each term $(a_i - t b_i)^2 \ge 0$ for all real $t$, their sum is also non-negative: $f(t) \ge 0$.
3.  **Expansion of the Quadratic**
    * **Claim:** $f(t) = (\sum b_i^2)t^2 - 2(\sum a_i b_i)t + (\sum a_i^2)$.
    * **Justification:** By the algebraic identity $(x - y)^2 = x^2 - 2xy + y^2$ and the linearity of summation:
        $$f(t) = \sum_{i=1}^n (a_i^2 - 2t a_i b_i + t^2 b_i^2) = \sum a_i^2 - 2t \sum a_i b_i + t^2 \sum b_i^2$$
4.  **Discriminant Condition**
    * **Claim:** For a quadratic $At^2 + Bt + C \ge 0$ to hold for all real $t$ where $A > 0$, the discriminant $D = B^2 - 4AC$ must satisfy $D \le 0$.
    * **Justification:** If $D > 0$, the quadratic would have two distinct real roots and take negative values between them, contradicting $f(t) \ge 0$.
    * **Mapping:** Here, $A = \sum b_i^2$, $B = -2\sum a_i b_i$, and $C = \sum a_i^2$.
5.  **Application of the Discriminant**
    * **Claim:** $(-2\sum a_i b_i)^2 - 4(\sum b_i^2)(\sum a_i^2) \le 0$.
    * **Justification:** Substitution of the coefficients into the discriminant formula $D \le 0$.
6.  **Algebraic Rearrangement**
    * **Claim:** $4(\sum a_i b_i)^2 \le 4(\sum b_i^2)(\sum a_i^2)$.
    * **Justification:** Expand the square $(-2)^2 = 4$ and move the negative term to the right side of the inequality.
7.  **Final Simplification**
    * **Claim:** $(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
    * **Justification:** Divide both sides by the positive constant 4.

Equality Case:
Equality holds if and only if $f(t) = 0$ for some $t$. This occurs if $a_i - t b_i = 0$ for all $i$, meaning the sequences $(a_i)$ and $(b_i)$ are proportional (or if one sequence is all zeros).

Final Conclusion:
$(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$
