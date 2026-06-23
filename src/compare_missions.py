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
        "risk_changes": changes
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