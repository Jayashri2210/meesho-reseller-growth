Narrative Report
1. Worked Narrative — May Ethnic Wear
Context

This measures revenue for Ethnic Wear from April to May 2026. The comparison is May versus April.

Insight

Fact: Ethnic Wear revenue increased from INR 104520.77 in April to INR 185107.61 in May, representing 77.1% MoM growth. This result is flagged because the absolute MoM movement is greater than the 8% threshold.

Implication

Hypothesis: The large increase may indicate stronger reseller demand or a shift in category mix toward Ethnic Wear, but the revenue data alone does not establish the cause.

Action: A regional manager should review May Ethnic Wear reseller activity and category-level order volume next, then identify which regions contributed most to the increase before deciding whether to increase category focus.

Refinement Self-Score

Specificity: Pass — the narrative names Ethnic Wear, April, May, INR 104520.77, INR 185107.61, and 77.1% exactly.

Audience fit: Pass — the wording focuses on what a regional manager should review and decide rather than on implementation details.

Completeness: Pass — Context, Insight, and Implication are all present.

Actionability: Pass — the next step is to review reseller activity, order volume, and regional contribution before deciding on category focus.

2. Worked Narrative — June Ethnic Wear
Context

This measures revenue for Ethnic Wear from May to June 2026. The comparison is June versus May.

Insight

Fact: Ethnic Wear revenue decreased from INR 185107.61 in May to INR 76371.53 in June, representing -58.74% MoM growth. This result is flagged because the absolute MoM movement is greater than the 8% threshold.

Implication

Hypothesis: The decline may indicate weaker category demand or a change in reseller/category mix, but the revenue data alone does not prove the cause.

Action: A regional manager should review June Ethnic Wear reseller activity and order volume against May, with particular attention to regions that contributed to the decline, before taking corrective action.

Refinement Self-Score

Specificity: Pass — the narrative names Ethnic Wear, May, June, INR 185107.61, INR 76371.53, and -58.74% exactly.

Audience fit: Pass — the recommendation is framed for a regional manager making an operational decision.

Completeness: Pass — Context, Insight, and Implication are all present.

Actionability: Pass — the next step specifically identifies reseller activity, order volume, and regional contribution for review.

3. Chart-Choice Justification
Question 1 — Which month had the highest total revenue?

A column chart is the clearest choice because this is a univariate comparison of total revenue across three months. Each month is one category and revenue is the measured value. The y-axis should start at zero so the differences are not visually exaggerated, and the three bars make it clear within 10 seconds that May has the highest total revenue at INR 444594.25, compared with April at INR 419417.43 and June at INR 398055.24. No legend is necessary because there is only one series.

Question 2 — What percentage share does Ethnic Wear represent of April's total revenue?

A single stacked bar or 100% stacked bar would be appropriate if showing Ethnic Wear's share against the other April categories, because the question concerns one part-to-whole relationship. The relevant verified values are INR 104520.77 for Ethnic Wear and INR 419417.43 for April total revenue, giving a 24.92% share. The visual should make the part-to-whole message clear within 10 seconds, use a zero-based scale where applicable, avoid 3D effects, and use a legend only if multiple category segments require identification.

Question 3 — How do the four regions compare on total revenue?

A column chart is appropriate because this is a univariate comparison of one measure, total revenue, across four regions. The values are North INR 337125.46, West INR 333106.33, South INR 316736.68, and East INR 275098.45. Starting the y-axis at zero prevents the regional differences from being exaggerated and allows the regional ranking to be understood within 10 seconds. Since there is only one revenue series, a legend is unnecessary.

4. Masked Top-Reseller Narrative

Fact: The five resellers exceeding the INR 50000 total-spend threshold are represented below using coded aliases rather than raw reseller names.

West — ALIAS-19: INR 75295.09 total spend.

West — ALIAS-22: INR 73882.33 total spend.

South — ALIAS-12: INR 69936.46 total spend.

North — ALIAS-06: INR 64238.97 total spend.

North — ALIAS-05: INR 61825.02 total spend.

Implication: A regional manager should review these high-spend reseller accounts for repeatable category and regional patterns and use the coded aliases when sharing any external-facing summary.

Hypothesis: The concentration of high-spend resellers in particular regions may indicate opportunities for targeted reseller support, but the top-spender data alone does not prove the cause of the regional differences.

5. Masking Validation

The masking policy requires raw reseller names to be excluded from external-facing narrative text.

The alias function is expected to produce:

RS019 → ALIAS-19

The final top-reseller narrative above uses aliases only and contains no raw reseller names, so assert_no_raw_names_leak should return True for the final narrative.

For the negative test, a version containing the raw string Mumbai Reseller 1 should cause assert_no_raw_names_leak to return False.
