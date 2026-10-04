import csv
import json
import os
import sys


# Allow this script to import the Part 2 engine when run from the
# repository root or directly from the part4_agent folder.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART2_DIR = os.path.join(ROOT_DIR, "part2_engine")

if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

from growth_engine import mom_growth, is_flagged, validate_feed


def load_revenue_feed(csv_path: str) -> dict[str, float]:
    """Load category revenue values from a validated monthly feed."""
    revenue = {}

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            revenue[row["category"]] = float(row["revenue"])

    return revenue


def fill_prompt(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Deterministic offline implementation of the Part 3 prompt-pack template.

    Only verified supplied values are used. The message intentionally
    contains no additional numeric figures.
    """
    return (
        f"Context: {category} revenue movement for {month} versus {prev_month}. "
        f"Insight — Fact: {category} recorded {mom_pct}% MoM growth. "
        f"Implication — Action: Review reseller activity and category order "
        f"patterns for this period before deciding the next operational action."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Run the guarded reseller-growth monitoring workflow."""

    # 1. Validate the current feed before anything else.
    validation_status, validation_errors = validate_feed(current_month_csv)

    # 2. Hard Stop if the current feed is invalid.
    if not validation_status:
        result = {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }
        return result

    # 3. Load verified previous and current revenue.
    previous = load_revenue_feed(previous_month_csv)
    current = load_revenue_feed(current_month_csv)

    flagged = []
    suppressed = []
    escalated = []

    # 4. Compute MoM growth and classify every category.
    for category, current_revenue in current.items():
        if category not in previous:
            continue

        previous_revenue = previous[category]
        mom_pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(mom_pct)

        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
        }

        if status == "flagged":
            flagged.append(item)
        elif status == "escalate_exact_boundary":
            escalated.append(category)

    # 5. Sort flagged categories by absolute MoM magnitude.
    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)

    # 6. Draft messages for at most the top 3 flagged categories.
    drafted_flagged = []

    for item in flagged[:3]:
        message = fill_prompt(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=_previous_month_name(month),
        )

        drafted_flagged.append(
            {
                "category": item["category"],
                "mom_pct": item["mom_pct"],
                "previous_revenue": item["previous_revenue"],
                "current_revenue": item["current_revenue"],
                "drafted": True,
                "message": message,
            }
        )

    # 7. Suppress flagged categories beyond the top-3 cap.
    for item in flagged[3:]:
        suppressed.append(item["category"])

    # 7b. Exact-boundary categories are already recorded separately above.

    # 8. Emit one structured JSON-compatible object.
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted_flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


def _previous_month_name(month: str) -> str:
    """Return the previous month used by the supplied three-month dataset."""
    month_order = {
        "April": "March",
        "May": "April",
        "June": "May",
    }
    return month_order.get(month, "previous month")


def main() -> None:
    """Run from the command line using three CSV paths."""

    if len(sys.argv) != 4:
        print(
            "Usage: python part4_agent/mock_agent_runner.py "
            "<month> <previous_month_csv> <current_month_csv>"
        )
        sys.exit(1)

    month = sys.argv[1]
    previous_month_csv = sys.argv[2]
    current_month_csv = sys.argv[3]

    result = run(
        month,
        previous_month_csv,
        current_month_csv,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
