def clamp_score(score):
    return max(0, min(100, round(score, 1)))


def get_factor(value, mapping):
    return mapping.get(value.lower(), 0)


def simulate_mission(duration_days, radiation, shielding, exercise):
    radiation_map = {
        "low": 10,
        "medium": 25,
        "high": 40
    }

    shielding_map = {
        "low": -5,
        "medium": -15,
        "high": -25
    }

    exercise_map = {
        "low": 15,
        "medium": 5,
        "high": -10
    }

    radiation_factor = get_factor(radiation, radiation_map)
    shielding_factor = get_factor(shielding, shielding_map)
    exercise_factor = get_factor(exercise, exercise_map)

    duration_factor = duration_days * 0.12

    dna_damage = duration_factor + radiation_factor + shielding_factor
    mitochondrial_stress = (
        duration_factor * 0.9
        + radiation_factor * 0.7
        + exercise_factor
    )

    immune_dysfunction = (
        duration_factor * 0.6
        + radiation_factor * 0.4
        + exercise_factor
    )

    inflammation = (
        duration_factor * 0.5
        + radiation_factor * 0.5
        + exercise_factor
    )

    senescence = (
        duration_factor * 0.8
        + radiation_factor * 0.6
        + shielding_factor * 0.5
    )

    return {
        "dna_damage": clamp_score(dna_damage),
        "mitochondrial_stress": clamp_score(mitochondrial_stress),
        "immune_dysfunction": clamp_score(immune_dysfunction),
        "inflammation": clamp_score(inflammation),
        "senescence": clamp_score(senescence)
    }


if __name__ == "__main__":
    result = simulate_mission(
        duration_days=180,
        radiation="high",
        shielding="medium",
        exercise="low"
    )

    print(result)
