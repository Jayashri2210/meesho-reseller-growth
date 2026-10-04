Part 4 — Agent Specification
Goal

Keep Meesho category managers informed of category revenue movements beyond the 8% month-on-month threshold, while ensuring every drafted message is held for human approval before use.

Tools

The monitoring agent calls:

validate_feed from Part 2 to validate the monthly revenue CSV before processing.

mom_growth from Part 2 to calculate month-on-month revenue growth.

is_flagged from Part 2 to classify the growth result against the 8% threshold.

The Part 3 prompt-pack template-fill logic to create stakeholder-ready draft messages.

The Part 3 masking logic when reseller information is included in a narrative.

Memory / State

Between runs, the agent must retain the previous month's verified revenue per category. This previous-month state is required to calculate the next month's month-on-month growth.

The agent also retains the verified current-month feed and the run month so that each calculation can be traced back to the relevant Part 1 output.

Planner

The agent performs these subtasks in order:

Load the monthly revenue feed and run validate_feed.

If validation fails, Hard Stop and report the validation errors.

If validation succeeds, compute mom_growth for every category against the previous month.

Run is_flagged on every category.

Sort flagged categories by absolute MoM percentage in descending order.

Draft a message using the Part 3 template for at most the top 3 flagged categories by magnitude. This cap prevents notification flooding.

Log any remaining flagged categories beyond the cap as suppressed, review manually without drafting a message for them.
7b. Separately log every category whose result is escalate_exact_boundary into escalated_categories. These categories must not be silently dropped or treated as either flagged or not flagged.

Emit one structured JSON object for the run.

Feedback Loop

Every drafted message is held for human approval.

The mock runner does not send email, call Gmail, use SMTP, or make any network request. The output records that the draft was created and held for approval.

A human reviewer must approve the message before it could be considered ready for external use.

Input Guardrail

validate_feed must pass before any growth calculation, classification, or narrative drafting takes place.

If validation returns False, the agent performs a Hard Stop.

The validation errors must be surfaced in the structured output.

Action Guardrail

No message is ever automatically sent.

The agent only drafts messages and holds them for human approval.

Output Guardrail

Every number in a drafted message must trace back to a verified Part 1 or Part 2 value.

The agent must never invent a revenue amount, percentage, order count, date, or other numeric figure.

Raw reseller names must not appear in an external-facing narrative. Resellers must be represented using coded aliases.

Success and Error Stopping Conditions
Success

A successful run produces drafted messages for the highest-magnitude flagged categories, up to the maximum of three, or correctly produces zero drafts when no category crosses the threshold.

Every number in every draft must be traceable to verified input data.

Suppressed flagged categories are explicitly logged.

Exact-boundary categories are separately logged in escalated_categories.

Error

If validate_feed returns False, the run is a Hard Stop.

No MoM calculation or message drafting is attempted.

The validation errors are returned in validation_errors.

Given-When-Then Agent Specifications
Scenario 1 — May Ethnic Wear

Given April Ethnic Wear revenue is INR 104520.77 and May Ethnic Wear revenue is INR 185107.61.

When the agent calculates MoM growth and applies the threshold rule.

Then mom_growth returns 77.1 and is_flagged returns "flagged", so Ethnic Wear is eligible for drafting.

Scenario 2 — June Beauty & Personal Care

Given May Beauty & Personal Care revenue is INR 35542.11 and June revenue is INR 37559.07.

When the agent evaluates the category.

Then mom_growth returns 5.67 and is_flagged returns "not_flagged", so the category is not drafted and is not suppressed.

Scenario 3 — Exact Boundary

Given previous revenue is 100000 and current revenue is 108000.

When the agent evaluates the category.

Then mom_growth returns exactly 8.0 and is_flagged returns "escalate_exact_boundary", so the category is placed in escalated_categories and no message is drafted.

Scenario 4 — Invalid Feed

Given the current feed contains the three validation errors in the corrupted fixture.

When the agent runs validate_feed.

Then validation returns False, the exact errors are surfaced, flagged_categories and suppressed_categories remain empty, and the run ends with action_taken equal to "hard_stop".

Structured Output

Every run emits one JSON object with exactly these top-level keys:

run_month

validation_status

validation_errors

flagged_categories

suppressed_categories

escalated_categories

action_taken

For a drafted category, the corresponding object in flagged_categories contains:

category

mom_pct

previous_revenue

current_revenue

drafted

message

The allowed success action is:

drafted_and_held_for_approval

The allowed validation failure action is:

hard_stop
