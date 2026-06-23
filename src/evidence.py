import json


EVIDENCE_PATH = "data/pathway_evidence.json"


def load_pathway_evidence():
    with open(EVIDENCE_PATH, "r") as file:
        return json.load(file)


def interpret_risk_scores(risk_scores):
    evidence = load_pathway_evidence()
    interpretations = {}

    for risk_key, score in risk_scores.items():
        if risk_key not in evidence:
            continue

        risk_info = evidence[risk_key]

        if score >= 70:
            risk_level = "High"
        elif score >= 45:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        interpretations[risk_key] = {
            "display_name": risk_info["display_name"],
            "score": score,
            "risk_level": risk_level,
            "pathways": risk_info["pathways"],
            "interpretation": risk_info["interpretation"],
            "why_it_matters": risk_info["why_it_matters"]
        }

    return interpretations


if __name__ == "__main__":
    sample_scores = {
        "dna_damage": 78.8,
        "mitochondrial_stress": 82.4,
        "immune_dysfunction": 57.3,
        "inflammation": 56.9,
        "senescence": 56.5
    }

    results = interpret_risk_scores(sample_scores)

    for key, item in results.items():
        print(f"\n{item['display_name']}")
        print(f"Score: {item['score']}")
        print(f"Risk Level: {item['risk_level']}")
        print("Pathways:", ", ".join(item["pathways"]))
        print("Interpretation:", item["interpretation"])
        print("Why it matters:", item["why_it_matters"])