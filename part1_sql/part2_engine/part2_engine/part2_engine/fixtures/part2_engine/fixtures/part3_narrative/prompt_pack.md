Reusable Prompt Pack — Significant Category Change
Trigger

Start this prompt when a category's is_flagged result is exactly "flagged".

The prompt is used to create a stakeholder-ready update for a category whose month-on-month revenue change has crossed the defined 8% threshold.

Input list

The prompt requires these verified placeholder variables:

{category} — category name.

{previous_revenue} — revenue for the previous month.

{current_revenue} — revenue for the current month.

{mom_pct} — calculated month-on-month percentage.

{month} — current month.

{prev_month} — previous month.

{region} — optional region context when a region-specific update is required.

{alias} — optional coded reseller alias when a reseller must be referenced.

Only supplied and verified values may be used.

Prompt

Write a concise stakeholder update using the following structure:

Context

State what category is being measured and explicitly name the comparison period as {month} versus {prev_month}.

Insight

State the verified revenue movement using only the supplied placeholders {previous_revenue}, {current_revenue}, and {mom_pct}. Label the numerical observation explicitly as a Fact.

Implication

Give one specific, actionable next step for the stakeholder. If a possible cause is suggested but is not directly demonstrated by the supplied data, label that statement explicitly as a Hypothesis.

Do not invent, estimate, round differently, or infer any number that is not supplied in the input placeholders.

Never introduce a reseller's raw name. If a reseller must be referenced, use only {alias} and the supplied region.

Every numerical statement must trace directly to one of the supplied verified placeholders.

Keep the message concise and suitable for a regional or category manager.

Checklist

Before the narrative is used, verify all of the following:

Every number in the draft exactly matches a supplied verified placeholder value.

The category name and comparison months match the supplied inputs.

The numerical observation is explicitly labeled as a Fact.

Any proposed cause or explanation that is not proven by the data is explicitly labeled as a Hypothesis.

The recommendation is specific and actionable rather than a vague instruction to "look into" the category.

No raw reseller name appears in the narrative; coded aliases are used instead.

The narrative follows the Context → Insight → Implication structure.

The message does not introduce unsupported metrics, percentages, dates, or quantities.
