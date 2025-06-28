# Test Set Evaluation Report

Below are the key performance numbers from running my logistic‐regression model on the hold‐out 20% test set of BB5 machines.

---

## 1. Overall Accuracy

-   **Value:** 0.2670
-   **Definition:**  
    \[
    \text{Accuracy} = \frac{\text{# correct predictions}}{\text{total # predictions}}
    \]
-   **Interpretation:**  
    Only 26.7 % of machines were classified correctly (halt vs. nonhalt).  
    In heavily imbalanced data (many more nonhalt than halt), high accuracy is hard to reach.

---

## 2. Precision (for the “halt” class)

-   **Value:** 0.2667
-   **Definition (for halt):**  
    \[
    \text{Precision} = \frac{\text{true halts predicted halt}}{\text{all predicted halt}}
    \]
-   **Interpretation:**  
    Of every 100 machines our model labels “halt,” only about 27 actually halt.

---

## 3. Recall (for the “halt” class)

-   **Value:** 0.9989
-   **Definition (for halt):**  
    \[
    \text{Recall} = \frac{\text{true halts predicted halt}}{\text{all actual halt}}
    \]
-   **Interpretation:**  
    Our model catches nearly all of the true halting machines (99.9 % of them).

---

## 4. F₁ Score (for the “halt” class)

-   **Value:** 0.4209
-   **Definition:** harmonic mean of precision and recall  
    \[
    F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
    \]
-   **Interpretation:**  
    Balances our very high recall with low precision—overall F₁ is 0.42.

---

## 5. Confusion Matrix

Rows = **true** labels; Columns = **predicted** labels

|                  | Predicted nonhalt | Predicted halt |
| ---------------- | ----------------- | -------------- |
| **True nonhalt** | 22 015            | 26 582 221     |
| **True halt**    | 10 545            | 9 665 863      |

-   **22 015** true nonhalt machines were correctly predicted nonhalt.
-   **26 582 221** true nonhalt were mistakenly predicted halt.
-   **10 545** true halt were missed (predicted nonhalt).
-   **9 665 863** true halt were correctly predicted halt.

---

## 6. Class Support

-   **Actual halts:** 9 676 408
-   **Actual nonhalts:** 26 604 236

---

### Summary

-   The model is **extremely** sensitive to halting machines (Recall ≈ 99.9 %) but labels almost everything “halt” (very low Precision ≈ 27 %), yielding poor overall accuracy (≈ 27 %).
