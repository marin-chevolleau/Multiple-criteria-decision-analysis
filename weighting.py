import pandas as pd

from criterion import Criterion

from normalize import normalize

def compute_weights(df: pd.DataFrame, weights: dict[str, Criterion]) -> pd.DataFrame:
    """
    Return a dataframe with a column containing the weighted sum of the criteria
    """
    weighted_df: pd.DataFrame = df.copy()

    # Multiply each criterion by its weight and sum the results
    for criterion, descriptors in weights.items():
        weighted_df[criterion] = weighted_df[criterion] * descriptors.weight

    # Create a new column for the weighted sum with 4 decimals
    weighted_df["Weighted sum"] = (
        weighted_df[list(weights.keys())].sum(axis=1).round(4)
    )

    # Drop the criterion columns
    weighted_df = weighted_df.drop(columns=list(weights.keys()))

    # Order the dataframe by the weighted sum
    weighted_df = weighted_df.sort_values(by="Weighted sum")

    return weighted_df


if __name__ == "__main__":
    input_path = "data/"
    output_path = "output/"

    initial_solutions: pd.DataFrame = pd.read_csv(
        #output_path + "preanalysed_solutions_satisfaction.csv"
        output_path + "preanalysed_solutions_dominance.csv"
    )
    
    weights: dict = {
        "C1": Criterion("minimize", weight=1),
        "C2": Criterion("minimize", weight=2),
        "C3": Criterion("maximize", weight=4),
        "C4": Criterion("minimize", weight=5),
        "C5": Criterion("minimize", weight=3),
        "C6": Criterion("maximize", weight=5),
        "C7": Criterion("maximize", weight=4),
    }

    normalized_solutions: pd.DataFrame = normalize(initial_solutions, weights)
    weighted_solutions: pd.DataFrame = compute_weights(normalized_solutions, weights)

    weighted_solutions.to_csv(output_path + "weighted_solutions.csv", index=False)
