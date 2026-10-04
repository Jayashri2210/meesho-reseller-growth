Meesho Reseller Growth & Alert Intelligence Pipeline
Project Overview

This repository contains an end-to-end reseller growth-monitoring pipeline for Meesho-style reseller operations.

The pipeline combines:

SQL business queries for verified revenue and reseller metrics.

A Python growth engine with explicit 8% significance rules and input validation.

A deterministic offline narrative layer using reusable templates.

A guarded mock agent that validates data, calculates growth, limits drafted alerts, and holds every message for human approval.

The complete workflow runs locally with zero API keys, zero paid services, and zero account-gated services.

Repository Structure
meesho-reseller-growth-pipeline/
├── README.md
├── data/
│   └── generate_dataset.py
├── part1_sql/
│   └── queries.sql
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
└── part4_agent/
    ├── agent_spec.md
    └── mock_agent_runner.py

Requirements

Python 3.10 or later.

SQLite3, included with Python.

No external Python packages are required.

No API keys are required.

No paid or hosted service is required.

Run the Pipeline in Order
Step 1 — Generate the dataset

The dataset generator is the fixed seeded script supplied in the project brief.

From the repository root, run:

python data/generate_dataset.py


This creates:

data/resellers.csv
data/orders.csv
data/meesho_reseller.db


The generated dataset contains 24 resellers and 900 orders.

The random seed is fixed at 42, so regeneration produces the same data.

Step 2 — Run Part 1 SQL

The SQL business queries are stored in:

part1_sql/queries.sql


The database created by Step 1 is:

data/meesho_reseller.db


To inspect the SQL manually using SQLite:

sqlite3 data/meesho_reseller.db


Then paste the queries from:

part1_sql/queries.sql


The five business questions covered are:

Monthly revenue by category.

Region-wise revenue and order count.

Top resellers by total spend.

Resellers who have never placed an order, including the COUNT(*) versus COUNT(order_id) demonstration.

June Delivered-order Average Order Value.

The required monthly category output is stored as the validated fixture:

part2_engine/fixtures/monthly_category_revenue.csv

Step 3 — Run Part 2 tests

From the repository root:

python -m unittest discover -s part2_engine -p "test_growth_engine.py"


The Part 2 engine implements:

mom_growth(previous, current)

is_flagged(mom_pct, threshold=8.0)

validate_feed(csv_path)

The threshold behavior is:

abs(mom_pct) > 8.0  -> flagged
abs(mom_pct) < 8.0  -> not_flagged
abs(mom_pct) == 8.0 -> escalate_exact_boundary


The corrupted fixture is:

part2_engine/fixtures/corrupted_feed.csv


The validated Part 1 monthly feed is:

part2_engine/fixtures/monthly_category_revenue.csv

Step 4 — Review Part 3 narrative outputs

Part 3 is deterministic and offline.

The reusable prompt pack is:

part3_narrative/prompt_pack.md


The worked narrative and chart-choice report is:

part3_narrative/narrative_report.md


The reseller masking functions are:

part3_narrative/masking.py


Run the masking checks with:

python part3_narrative/masking.py


The masking layer ensures that raw reseller names are not exposed in external-facing narrative text.

Step 5 — Run Part 4 mock agent

The mock agent is:

part4_agent/mock_agent_runner.py


For the May scenario, run:

python part4_agent/mock_agent_runner.py May part2_engine/fixtures/monthly_category_revenue.csv part2_engine/fixtures/monthly_category_revenue.csv


For an actual April-to-May run, the previous and current month feeds should contain the appropriate month-specific rows.

For a June scenario, the same runner accepts the corresponding May and June feeds.

The runner performs:

Feed validation.

Hard Stop on invalid input.

Month-on-month calculation.

Threshold classification.

Sorting by absolute MoM magnitude.

Drafting for at most three flagged categories.

Suppression logging for additional flagged categories.

Separate exact-boundary escalation.

Structured JSON output.

Every drafted message is held for human approval. There is no email or automatic sending integration.

Expected Business Results

The seeded dataset produces these key results.

May versus April

Ethnic Wear: 77.1% — flagged.

Western Wear: -23.6% — flagged.

Kids Wear: -23.48% — flagged.

Home & Kitchen: -9.25% — flagged.

Beauty & Personal Care: -12.75% — flagged.

The mock agent drafts the three largest movements by absolute percentage:

Ethnic Wear — 77.1%

Western Wear — -23.6%

Kids Wear — -23.48%

The remaining flagged categories are suppressed for manual review.

June versus May

Ethnic Wear: -58.74% — flagged.

Western Wear: 11.97% — flagged.

Kids Wear: 23.9% — flagged.

Home & Kitchen: 42.59% — flagged.

Beauty & Personal Care: 5.67% — not flagged.

The mock agent drafts:

Ethnic Wear — -58.74%

Home & Kitchen — 42.59%

Kids Wear — 23.9%

Western Wear is suppressed because it is the fourth-largest flagged movement.

Beauty & Personal Care is not included because its 5.67% movement is below the 8% threshold.

How the Parts Connect
Part 1 → Part 2

Part 1 computes the verified business numbers using SQL first. Part 2 then consumes the monthly category revenue output and applies explicit, testable growth and validation rules.

This mirrors the workflow pattern:

Compute real numbers first → validate and analyze second.

Part 2 → Part 3

Part 2 determines which movements are significant. Part 3 turns only those verified values into stakeholder-ready narrative using a deterministic template.

This prevents narrative generation from inventing or changing business numbers.

Part 3 → Part 4

Part 4 uses the Part 3 template-fill approach to draft messages after the Part 2 guardrails have passed.

Part 4 also applies the masking policy when reseller information is used.

Part 4 workflow

The overall agent follows:

Intake → Validate → Summary → Classify → Report Draft → Suppress/Escalate → Human Review

The agent never automatically sends a message.

Guardrails
Input Guardrail

validate_feed must pass before growth calculations or drafting occur.

If validation fails:

validation_status = invalid
action_taken = hard_stop


No MoM computation is attempted.

Action Guardrail

All messages are drafts only.

The system does not send email and does not connect to Gmail, SMTP, or any external messaging service.

Output Guardrail

Every numeric value in a drafted message must trace back to verified Part 1 or Part 2 data.

The system does not invent figures.

Exact 8% boundary cases are escalated for human review rather than automatically classified as flagged or not flagged.

Offline / Zero-API-Key Operation

The complete project works with zero API keys set.

The AI-narrative portion is intentionally implemented as a deterministic offline template-fill function. No LLM API is required for grading or execution.

No paid subscription or hosted account is required.

Academic Integrity / Documentation Reference

The implementation uses Python standard-library functionality such as:

csv

sqlite3

random

unittest

json

os

sys

Official Python documentation was consulted for standard-library behavior where needed:

Python csv module documentation.

Python sqlite3 module documentation.

Python unittest module documentation.

Python json module documentation.

No external package or paid service is required.

Submission

The complete project is contained in this public GitHub repository.

The repository is intended to be run in the following order:

Part 1: Generate dataset + SQL
        ↓
Part 2: Validate feed + calculate growth
        ↓
Part 3: Generate/validate stakeholder narrative
        ↓
Part 4: Run guarded mock agent + human approval checkpoint
