Meesho Reseller Growth & Alert Intelligence Pipeline
Project Overview

This repository contains an end-to-end reseller growth-monitoring pipeline for Meesho-style reseller operations.

The pipeline connects four Parts:

Part 1 — SQL Business Query Engine: generates verified business metrics from the reseller/order dataset.

Part 2 — Python Guardrail & Growth Detection Engine: validates the SQL feed and calculates month-on-month growth using an explicit 8% threshold.

Part 3 — Reliable AI Narrative Layer: converts verified numbers into stakeholder-ready narratives using deterministic offline templates and protects reseller identities with aliases.

Part 4 — Agentic Workflow: connects Parts 1–3 into a guarded workflow that validates input, calculates growth, prioritizes alerts, drafts messages, and holds them for human approval.

The complete workflow is:

Dataset
   ↓
Part 1: SQL
   ↓
Verified monthly revenue CSV
   ↓
Part 2: Validation + MoM growth
   ↓
Part 3: Narrative + masking
   ↓
Part 4: Guarded mock agent
   ↓
Draft held for human approval

Requirements

Python 3.10 or newer recommended.

SQLite through Python's standard-library sqlite3 module.

No paid services are required.

No API key is required.

No hosted database is required.

No real email or messaging service is required.

The complete pipeline runs offline with zero API keys set.

Step 1 — Generate the Dataset

The supplied seeded generator must be used without changing its seed, weights, or row counts.

From the repository root, run:

python data/generate_dataset.py


This creates:

data/resellers.csv
data/orders.csv
data/meesho_reseller.db


The generated dataset contains:

24 resellers

900 orders

300 April orders

300 May orders

300 June orders

The generator uses the fixed random seed 42, making the dataset reproducible.

Step 2 — Run Part 1

Part 1 contains the SQL business query engine.

Run:

python part1_sql/run_queries.py


This creates:

part1_sql/output/monthly_category_revenue.csv
part1_sql/output/region_revenue.csv
part1_sql/output/top_resellers.csv
part1_sql/output/zero_order_resellers.csv
part1_sql/output/zero_order_count_demo.csv
part1_sql/output/june_delivered_aov.csv


The main hand-off file for later Parts is:

part1_sql/output/monthly_category_revenue.csv


It contains:

month,category,revenue,n_orders


This file is consumed by Part 2 and Part 4.

Part 1 answers the five required business questions:

Monthly revenue by category.

Region-wise revenue and order count.

Top resellers by total spend.

Resellers with no orders.

June delivered Average Order Value.

The zero-order query also demonstrates why COUNT(*) is not suitable for detecting an unmatched LEFT JOIN row. For RS024, the result is COUNT(*) = 1 but COUNT(order_id) = 0.

Step 3 — Run Part 2

Part 2 is implemented in:

part2_engine/growth_engine.py


It provides:

mom_growth()
is_flagged()
validate_feed()


The 8% rule is:

greater than 8% absolute change → flagged

less than 8% absolute change → not_flagged

exactly 8% absolute change → escalate_exact_boundary

Copy the validated Part 1 feed into the Part 2 fixtures:

cp part1_sql/output/monthly_category_revenue.csv part2_engine/fixtures/monthly_category_revenue.csv


On Windows PowerShell:

Copy-Item part1_sql/output/monthly_category_revenue.csv part2_engine/fixtures/monthly_category_revenue.csv


Run the tests:

python -m unittest part2_engine.test_growth_engine


The corrupted feed fixture is:

part2_engine/fixtures/corrupted_feed.csv


It must produce exactly three validation errors.

Step 4 — Part 3 Narrative Layer

Part 3 contains:

part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py


The prompt pack defines the reusable narrative structure.

The narrative report contains worked May and June Ethnic Wear examples using the verified Part 1 and Part 2 numbers.

The masking module prevents raw reseller names from appearing in external-facing narratives.

For example:

RS019 → ALIAS-19


The narrative layer is deterministic and fully offline. It does not require an LLM API.

Step 5 — Run Part 4

Part 4 connects the previous Parts into a guarded mock agent.

The specification is:

part4_agent/agent_spec.md


The runner is:

part4_agent/mock_agent_runner.py


The agent performs these operations:

Load the monthly revenue feed.

Validate the feed.

Hard Stop if validation fails.

Calculate MoM growth for every category.

Apply the 8% flagging rule.

Sort flagged categories by absolute growth magnitude.

Draft messages for at most the top three flagged categories.

Record additional flagged categories as suppressed for manual review.

Record exact-boundary categories separately in escalated_categories.

Emit one structured JSON result.

No message is automatically sent.

Successful runs use:

drafted_and_held_for_approval


and require human approval before any communication would be considered sent.

Running the Agent

The runner exposes:

run(month, previous_month_csv, current_month_csv)


The previous-month and current-month files should contain the same schema as the Part 1 monthly revenue output.

For the May scenario, the previous month is April and the current month is May.

For the June scenario, the previous month is May and the current month is June.

Guardrails
Input Guardrail

validate_feed() must pass before growth calculations or narrative drafting begin.

If validation fails, the agent performs a Hard Stop and surfaces the validation errors.

Action Guardrail

The agent never automatically sends a message.

It only creates a draft and holds it for human approval.

Output Guardrail

Every number in a drafted message must trace back to verified Part 1 or Part 2 values.

No invented figures are allowed.

Exact 8% changes are escalated for human review.

Workflow Mapping
Part 1 → Part 2

This mirrors the "compute real numbers via SQL first, then hand off" order of operations.

Part 1 establishes the verified numerical source of truth before Part 2 performs business-rule calculations.

Part 2 → Part 3

This separates calculation from explanation.

Part 2 determines whether a change is significant. Part 3 turns that verified result into a stakeholder-readable narrative without inventing numbers.

Part 3 → Part 4

This connects verified facts, narrative generation and governance.

The agent uses the validated calculations and narrative template while preserving masking rules.

Part 4

Part 4 mirrors an:

Intake → Validate → Compute → Prioritize → Report Draft → Human Validate


workflow.

The human approval checkpoint prevents an automated agent from directly communicating an unreviewed business message.

Zero API Keys

The complete pipeline works with:

API keys required: 0


No paid or account-gated service is required.

The narrative stage uses deterministic offline template filling rather than requiring a real LLM API.

Documentation Referenced

Implementation relies on Python standard-library documentation, including:

Python csv module documentation.

Python sqlite3 module documentation.

Python unittest documentation.

Python file I/O documentation.

No external API is required for the project.
