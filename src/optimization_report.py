from mission_optimizer import optimize_mission


def generate_report(baseline):

    optimization = optimize_mission(baseline)

    best = optimization["best_missions"][0]

    baseline_prediction = optimization["baseline_prediction"]
    best_prediction = best["prediction"]

    print("=" * 50)
    print("SPACEBIO TWIN OPTIMIZATION REPORT")
    print("=" * 50)

    print("\nMission Assessment")
    print("---------------------------")

    print(f"Baseline Overall Risk: {optimization['baseline_overall_risk']}")
    print(f"Optimized Overall Risk: {best['overall_risk']}")
    print(f"Improvement: {best['improvement']}")

    print("\nRecommended Mission")
    print("---------------------------")

    mission = best["mission"]

    print(f"Duration: {mission['duration_days']} days")
    print(f"Shielding: {mission['shielding']}")
    print(f"Exercise: {mission['exercise']}")

    print("\nLargest Biological Improvements")
    print("---------------------------")

    baseline_scores = baseline_prediction["risk_scores"]
    optimized_scores = best_prediction["risk_scores"]

    improvements = []

    for key in baseline_scores:

        diff = baseline_scores[key] - optimized_scores[key]

        improvements.append(
            (
                diff,
                key,
                baseline_scores[key],
                optimized_scores[key]
            )
        )

    improvements.sort(reverse=True)

    for diff, key, before, after in improvements:

        pretty = key.replace("_", " ").title()

        print(f"{pretty}: {before} → {after}")

    print("\nRecommended Actions")
    print("---------------------------")

    if mission["shielding"] != baseline["shielding"]:
        print("✓ Increase spacecraft shielding")

    if mission["exercise"] != baseline["exercise"]:
        print("✓ Increase astronaut exercise")

    if mission["duration_days"] != baseline["duration_days"]:
        print("✓ Reduce mission duration")
    
if __name__ == "__main__":
    baseline = {
        "duration_days": 365,
        "radiation": "high",
        "shielding": "low",
        "exercise": "low"
    }
        
generate_report(baseline)