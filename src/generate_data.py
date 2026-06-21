import random
import pandas as pd

from simulator import simulate_mission

rows = []

for _ in range(5000):
    duration = random.randint(30, 730)
    radiation = random.choice(["low", "medium", "high"])
    shielding = random.choice(["low", "medium", "high"])
    exercise = random.choice(["low", "medium", "high"])

    risks = simulate_mission(
        duration_days=duration,
        radiation=radiation,
        shielding=shielding,
        exercise=exercise
    )

    rows.append({
        "duration_days": duration,
        "radiation": radiation,
        "shielding": shielding,
        "exercise": exercise,
        **risks
    })

df = pd.DataFrame(rows)
df.to_csv("data/synthetic_missions.csv", index=False)

print(df.head())
print("\nSaved:", len(df), "missions to data/synthetic_missions.csv")