from predict import predict_mission


def overall_risk_score(risk_scores):
    return round(sum(risk_scores.values()) / len(risk_scores), 1)


def generate_candidate_missions(baseline):
    candidates = []

    durations = [baseline["duration_days"], 270, 180]
    shielding_levels = ["low", "medium", "high"]
    exercise_levels = ["low", "medium", "high"]

    for duration in durations:
        for shielding in shielding_levels:
            for exercise in exercise_levels:
                candidate = {
                    "duration_days": duration,
                    "radiation": baseline["radiation"],
                    "shielding": shielding,
                    "exercise": exercise
                }

                candidates.append(candidate)

    return candidates


def optimize_mission(baseline):
    baseline_prediction = predict_mission(**baseline)
    baseline_score = overall_risk_score(
        baseline_prediction["risk_scores"]
    )

    candidates = generate_candidate_missions(baseline)

    results = []

    for candidate in candidates:
        prediction = predict_mission(**candidate)
        score = overall_risk_score(prediction["risk_scores"])
        improvement = round(baseline_score - score, 1)

        results.append({
            "mission": candidate,
            "overall_risk": score,
            "improvement": improvement,
            "risk_scores": prediction["risk_scores"],
            "prediction": prediction
        })

    results = sorted(
        results,
        key=lambda x: x["overall_risk"]
    )

    return {
        "baseline_mission": baseline,
        "baseline_overall_risk": baseline_score,
        "baseline_prediction": baseline_prediction,
        "best_missions": results[:5],
        "summary": summarize_optimization({
        "baseline_overall_risk": baseline_score,
        "best_missions": results[:5]
        
})
    }

def summarize_optimization(optimization):
    baseline_score = optimization["baseline_overall_risk"]
    best = optimization["best_missions"][0]

    best_score = best["overall_risk"]
    improvement = best["improvement"]
    percent_improvement = round((improvement / baseline_score) * 100, 1)

    mission = best["mission"]

    summary = (
        f"The optimizer reduced predicted overall biological risk "
        f"from {baseline_score} to {best_score}, a {percent_improvement}% improvement. "
        f"The best mission profile uses {mission['duration_days']} days, "
        f"{mission['shielding']} shielding, and {mission['exercise']} exercise compliance."
    )

    return summary

if __name__ == "__main__":
    baseline_mars_mission = {
        "duration_days": 365,
        "radiation": "high",
        "shielding": "low",
        "exercise": "low"
    }

    optimization = optimize_mission(baseline_mars_mission)

    print("\nBaseline Mission:")
    print(optimization["baseline_mission"])
    print("Baseline Overall Risk:", optimization["baseline_overall_risk"])

    print("\nTop Optimized Missions:")
    for idx, result in enumerate(optimization["best_missions"], start=1):
        print(f"\nRank #{idx}")
        print("Mission:", result["mission"])
        print("Overall Risk:", result["overall_risk"])
        print("Improvement:", result["improvement"])
        print("Risk Scores:", result["risk_scores"])
        
    print("\nOptimization Summary:")
    print(optimization["summary"])
