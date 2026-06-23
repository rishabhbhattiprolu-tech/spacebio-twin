import pandas as pd
import joblib

from countermeasures import generate_countermeasures

MODEL_PATH = "data/spacebio_twin_model.pkl"


def predict_mission(duration_days, radiation, shielding, exercise):
    saved_model = joblib.load(MODEL_PATH)

    model = saved_model["model"]
    feature_columns = saved_model["feature_columns"]

    mission = pd.DataFrame([{
        "duration_days": duration_days,
        "radiation": radiation,
        "shielding": shielding,
        "exercise": exercise
    }])

    mission_encoded = pd.get_dummies(mission)

    for col in feature_columns:
        if col not in mission_encoded.columns:
            mission_encoded[col] = 0

    mission_encoded = mission_encoded[feature_columns]

    prediction = model.predict(mission_encoded)[0]

    risk_scores = {
        "dna_damage": float(round(prediction[0], 1)),
        "mitochondrial_stress": float(round(prediction[1], 1)),
        "immune_dysfunction": float(round(prediction[2], 1)),
        "inflammation": float(round(prediction[3], 1)),
        "senescence": float(round(prediction[4], 1))
    }

    countermeasures = generate_countermeasures(risk_scores)

    return {
        "mission_profile": {
            "duration_days": duration_days,
            "radiation": radiation,
            "shielding": shielding,
            "exercise": exercise
        },
        "risk_scores": risk_scores,
        "countermeasure_hypotheses": countermeasures
    }


if __name__ == "__main__":
    result = predict_mission(
        duration_days=365,
        radiation="high",
        shielding="low",
        exercise="low"
    )

    print("\nMission Profile:")
    print(result["mission_profile"])

    print("\nPredicted Risk Scores:")
    print(result["risk_scores"])

    print("\nCountermeasure Hypotheses:")
    for item in result["countermeasure_hypotheses"]:
        print(f"\nTarget: {item['target']}")
        print(f"Risk Score: {item['risk_score']}")
        print(f"Priority: {item['priority']}")
        print(f"Hypothesis: {item['hypothesis']}")
        print(f"Rationale: {item['rationale']}")