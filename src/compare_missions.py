from predict import predict_mission


def calculate_change(baseline_scores, modified_scores):
    changes = {}

    for key in baseline_scores:
        baseline_value = baseline_scores[key]
        modified_value = modified_scores[key]
        difference = round(modified_value - baseline_value, 1)

        if difference < 0:
            direction = "decreased"
        elif difference > 0:
            direction = "increased"
        else:
            direction = "unchanged"

        changes[key] = {
            "baseline": baseline_value,
            "modified": modified_value,
            "difference": difference,
            "direction": direction
        }

    return changes


def summarize_comparison(risk_changes):
    decreased = []
    increased = []

    for risk, values in risk_changes.items():
        clean_name = risk.replace("_", " ").title()
        difference = values["difference"]

        if difference < 0:
            decreased.append((clean_name, abs(difference)))
        elif difference > 0:
            increased.append((clean_name, difference))

    decreased = sorted(decreased, key=lambda x: x[1], reverse=True)
    increased = sorted(increased, key=lambda x: x[1], reverse=True)

    summary_parts = []

    if decreased:
        top_decreases = decreased[:2]
        decrease_text = " and ".join(
            [f"{name} by {change} points" for name, change in top_decreases]
        )
        summary_parts.append(f"The modified mission reduced {decrease_text}.")

    if increased:
        top_increases = increased[:2]
        increase_text = " and ".join(
            [f"{name} by {change} points" for name, change in top_increases]
        )
        summary_parts.append(f"However, it increased {increase_text}.")

    if not summary_parts:
        return "The modified mission produced no major change in predicted biological risk."

    return " ".join(summary_parts)


def compare_missions(baseline_mission, modified_mission):
    baseline_prediction = predict_mission(**baseline_mission)
    modified_prediction = predict_mission(**modified_mission)

    changes = calculate_change(
        baseline_prediction["risk_scores"],
        modified_prediction["risk_scores"]
    )

    return {
        "baseline_mission": baseline_mission,
        "modified_mission": modified_mission,
        "baseline_risks": baseline_prediction["risk_scores"],
        "modified_risks": modified_prediction["risk_scores"],
        "risk_changes": changes,
        "summary": summarize_comparison(changes)
    }


if __name__ == "__main__":
    baseline_mars_mission = {
        "duration_days": 365,
        "radiation": "high",
        "shielding": "low",
        "exercise": "low"
    }

    improved_shielding_mission = {
        "duration_days": 365,
        "radiation": "high",
        "shielding": "high",
        "exercise": "low"
    }

    comparison = compare_missions(
        baseline_mars_mission,
        improved_shielding_mission
    )

    print("\nBaseline Mission:")
    print(comparison["baseline_mission"])

    print("\nModified Mission:")
    print(comparison["modified_mission"])

    print("\nRisk Score Changes:")
    for risk, values in comparison["risk_changes"].items():
        clean_name = risk.replace("_", " ").title()

        print(f"\n{clean_name}")
        print(f"Baseline: {values['baseline']}")
        print(f"Modified: {values['modified']}")
        print(f"Change: {values['difference']}")
        print(f"Direction: {values['direction']}")

    print("\nSummary:")
    print(comparison["summary"])