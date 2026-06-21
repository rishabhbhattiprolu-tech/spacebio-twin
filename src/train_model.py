import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib


DATA_PATH = "data/synthetic_missions.csv"
MODEL_PATH = "data/spacebio_twin_model.pkl"


def train_model():
    df = pd.read_csv(DATA_PATH)

    features = df[[
        "duration_days",
        "radiation",
        "shielding",
        "exercise"
    ]]

    targets = df[[
        "dna_damage",
        "mitochondrial_stress",
        "immune_dysfunction",
        "inflammation",
        "senescence"
    ]]

    features_encoded = pd.get_dummies(features)

    x_train, x_test, y_train, y_test = train_test_split(
        features_encoded,
        targets,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    mae = mean_absolute_error(y_test, predictions)

    print("Model trained successfully.")
    print("Mean Absolute Error:", round(mae, 2))

    joblib.dump(
        {
            "model": model,
            "feature_columns": list(features_encoded.columns)
        },
        MODEL_PATH
    )

    print("Saved model to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()