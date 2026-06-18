def generate_countermeasures(risk_scores):
    countermeasures = []

    if risk_scores["dna_damage"] >= 45:
        countermeasures.append({
            "target": "DNA Damage",
            "risk_score": risk_scores["dna_damage"],
            "priority": "High" if risk_scores["dna_damage"] >= 70 else "Moderate",
            "hypothesis": "Increase radiation shielding and monitor DNA repair pathways.",
            "rationale": "Longer mission duration and higher radiation exposure increase predicted DNA damage risk."
        })

    if risk_scores["mitochondrial_stress"] >= 45:
        countermeasures.append({
            "target": "Mitochondrial Stress",
            "risk_score": risk_scores["mitochondrial_stress"],
            "priority": "High" if risk_scores["mitochondrial_stress"] >= 70 else "Moderate",
            "hypothesis": "Investigate mitochondrial-supportive countermeasures and metabolic stabilization strategies.",
            "rationale": "Spaceflight stress may disrupt mitochondrial and metabolic pathways."
        })

    if risk_scores["immune_dysfunction"] >= 45:
        countermeasures.append({
            "target": "Immune Dysfunction",
            "risk_score": risk_scores["immune_dysfunction"],
            "priority": "High" if risk_scores["immune_dysfunction"] >= 70 else "Moderate",
            "hypothesis": "Increase immune monitoring and evaluate exercise/nutrition-based support strategies.",
            "rationale": "Long-duration spaceflight can place stress on immune regulation."
        })

    if risk_scores["inflammation"] >= 45:
        countermeasures.append({
            "target": "Inflammation",
            "risk_score": risk_scores["inflammation"],
            "priority": "High" if risk_scores["inflammation"] >= 70 else "Moderate",
            "hypothesis": "Screen anti-inflammatory pathway countermeasures using perturbation-style databases.",
            "rationale": "Inflammatory signaling may rise under radiation, stress, and altered physiological conditions."
        })

    if risk_scores["senescence"] >= 45:
        countermeasures.append({
            "target": "Cellular Senescence",
            "risk_score": risk_scores["senescence"],
            "priority": "High" if risk_scores["senescence"] >= 70 else "Moderate",
            "hypothesis": "Monitor aging-associated biomarkers and evaluate senescence-related pathway interventions.",
            "rationale": "Prolonged spaceflight stress may overlap with biological aging signatures."
        })

    if not countermeasures:
        countermeasures.append({
            "target": "Overall Risk",
            "risk_score": "Low",
            "priority": "Low",
            "hypothesis": "No major countermeasure flagged under current simulator settings.",
            "rationale": "Predicted risk scores are below the current alert threshold."
        })

    return countermeasures


if __name__ == "__main__":
    from simulator import simulate_mission

    scores = simulate_mission(
        duration_days=180,
        radiation="high",
        shielding="medium",
        exercise="low"
    )

    suggestions = generate_countermeasures(scores)

    print("\nRisk Scores:")
    print(scores)

    print("\nCountermeasure Hypotheses:")
    for item in suggestions:
        print(f"\nTarget: {item['target']}")
        print(f"Risk Score: {item['risk_score']}")
        print(f"Priority: {item['priority']}")
        print(f"Hypothesis: {item['hypothesis']}")
        print(f"Rationale: {item['rationale']}")