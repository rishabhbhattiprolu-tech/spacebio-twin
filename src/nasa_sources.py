import pandas as pd


NASA_STUDIES_PATH = "data/nasa_studies.csv"


def load_nasa_studies():
    return pd.read_csv(NASA_STUDIES_PATH)


def get_studies_for_pathway(pathway_key):
    studies = load_nasa_studies()

    matches = studies[
        studies["pathway_relevance"].str.contains(pathway_key, na=False)
    ]

    return matches.to_dict(orient="records")


if __name__ == "__main__":
    for pathway in [
        "dna_damage",
        "mitochondrial_stress",
        "immune_dysfunction",
        "inflammation",
        "senescence"
    ]:
        print(f"\nPathway: {pathway}")
        results = get_studies_for_pathway(pathway)

        for study in results:
            print(f"- {study['study_id']}: {study['title']}")
            print(f"  Why used: {study['why_used']}")