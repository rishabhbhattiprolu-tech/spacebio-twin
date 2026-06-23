from predict import predict_mission


DISPLAY_NAMES = {
    "dna_damage": "DNA Damage",
    "mitochondrial_stress": "Mitochondrial Stress",
    "immune_dysfunction": "Immune Dysfunction",
    "inflammation": "Inflammation",
    "senescence": "Cellular Senescence"
}


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

    for risk, values in risk_changes.items():
        if values["difference"] < 0:
            decreased.append((DISPLAY_NAMES[risk], abs(values["difference"])))

    decreased = sorted(decreased, key=lambda x: x[1], reverse=True)

    if not decreased:
        return "The modified mission produced no major reduction in predicted biological risk."

    top_decreases = decreased[:2]
    decrease_text = " and ".join(
        [f"{name} by {change} points" for name, change in top_decreases]
    )

    return f"The modified mission reduced {decrease_text}."


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
        "risk_changes": changes,
        "summary": summarize_comparison(changes)
    }


def print_comparison(scenario_name, comparison):
    print(f"\n=== Scenario: {scenario_name} ===")

    print("\nModified Mission:")
    print(comparison["modified_mission"])

    print("\nRisk Score Changes:")
    for risk, values in comparison["risk_changes"].items():
        name = DISPLAY_NAMES[risk]
        print(
            f"{name}: {values['baseline']} → {values['modified']} "
            f"({values['difference']})"
        )

    print("\nSummary:")
    print(comparison["summary"])


if __name__ == "__main__":
    baseline_mars_mission = {
        "duration_days": 365,
        "radiation": "high",
        "shielding": "low",
        "exercise": "low"
    }

    scenarios = {
        "Improved Shielding": {
            "duration_days": 365,
            "radiation": "high",
            "shielding": "high",
            "exercise": "low"
        },
        "Improved Exercise": {
            "duration_days": 365,
            "radiation": "high",
            "shielding": "low",
            "exercise": "high"
        },
        "Shorter Mission": {
            "duration_days": 180,
            "radiation": "high",
            "shielding": "low",
            "exercise": "low"
        }
    }

    print("\nBaseline Mission:")
    print(baseline_mars_mission)

    for scenario_name, modified_mission in scenarios.items():
        comparison = compare_missions(
            baseline_mars_mission,
            modified_mission
        )

        print_comparison(scenario_name, comparison)