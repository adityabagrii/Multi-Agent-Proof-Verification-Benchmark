Assumptions:
- $a_1, a_2, \dots, a_n$ and $b_1, b_2, \dots, b_n$ are real numbers ($\mathbb{R}$).
- $n$ is a positive finite integer.

Proof Strategy:
The proof employs a quadratic polynomial argument. We first address the trivial case where the sum of squares of $b_i$ is zero to avoid division by zero. For the non-zero case, we define a non-negative quadratic function $f(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since a non-negative quadratic must have a non-positive discriminant, the inequality follows directly from the discriminant formula.

Numbered Proof Steps:
1.  **Case 1: $\sum_{i=1}^n b_i^2 = 0$**
    * **Claim:** If $\sum_{i=1}^n b_i^2 = 0$, the inequality holds as $0 \le 0$.
    * **Justification:** For real numbers, a sum of squares is zero if and only if each term is zero. Thus, $b_i = 0$ for all $i \in \{1, \dots, n\}$. Consequently, $\sum a_i b_i = 0$. Both sides of the inequality reduce to $0^2 \le (\sum a_i^2)(0)$, which is $0 = 0$.
2.  **Case 2: $\sum_{i=1}^n b_i^2 > 0$**
    * **Claim:** We can define a function $f(t) \ge 0$ for all $t \in \mathbb{R}$.
    * **Justification:** Let $f(t) = \sum_{i=1}^n (a_i - t b_i)^2$. Since each term $(a_i - t b_i)^2$ is a square of a real number, it is non-negative. The sum of non-negative terms is non-negative.
3.  **Expansion of the Quadratic**
    * **Claim:** $f(t) = (\sum_{i=1}^n b_i^2)t^2 - 2(\sum_{i=1}^n a_i b_i)t + (\sum_{i=1}^n a_i^2)$.
    * **Justification:** Expand the summand using the algebraic identity $(x - y)^2 = x^2 - 2xy + y^2$ and apply the linearity of summation: $\sum (a_i^2 - 2t a_i b_i + t^2 b_i^2)$.
4.  **Application of the Discriminant Rule**
    * **Claim:** For a quadratic $At^2 + Bt + C \ge 0$ with $A > 0$, the discriminant $D = B^2 - 4AC$ must satisfy $D \le 0$.
    * **Justification:** If $D > 0$, the quadratic would have two distinct real roots and would be negative between them, contradicting $f(t) \ge 0$. Here, $A = \sum b_i^2$, $B = -2\sum a_i b_i$, and $C = \sum a_i^2$.
5.  **Substitution and Simplification**
    * **Claim:** $(-2\sum_{i=1}^n a_i b_i)^2 - 4(\sum_{i=1}^n b_i^2)(\sum_{i=1}^n a_i^2) \le 0$.
    * **Justification:** Direct substitution of coefficients $A, B, C$ into the discriminant formula $B^2 - 4AC \le 0$.
6.  **Isolation of the Target Terms**
    * **Claim:** $4(\sum_{i=1}^n a_i b_i)^2 \le 4(\sum_{i=1}^n b_i^2)(\sum_{i=1}^n a_i^2)$.
    * **Justification:** From Step 5, $(-2\sum a_i b_i)^2 - 4(\sum b_i^2)(\sum a_i^2) \le 0$. Since $(-2X)^2=4X^2$, this is $4(\sum a_i b_i)^2 - 4(\sum b_i^2)(\sum a_i^2) \le 0$. Adding $4(\sum b_i^2)(\sum a_i^2)$ to both sides gives the claim.
7.  **Final Division**
    * **Claim:** $(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$.
    * **Justification:** Divide both sides of Step 6 by the positive constant $4$, which preserves the inequality direction, and commute the product on the right-hand side.

Equality Case:
Equality holds if and only if $f(t) = 0$ for some $t$. This occurs if $a_i - t b_i = 0$ for all $i$, meaning the sequences $(a_1, \dots, a_n)$ and $(b_1, \dots, b_n)$ are proportional.

Final Conclusion:
$(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2)(\sum_{i=1}^n b_i^2)$
