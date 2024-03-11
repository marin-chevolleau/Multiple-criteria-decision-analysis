import pandas as pd

from criterion import Criterion
from normalize import normalize

def compute_distances(df: pd.DataFrame, weights: dict[str, Criterion]):
    """
    Return a dataframe with the distances to the ideal and anti-ideal solutions appended
    """
    ideal_distances_df: pd.DataFrame = df.copy()
    anti_ideal_distances_df: pd.DataFrame = df.copy()

    for criterion in weights.keys():
        ideal_distances_df[criterion] = ideal_distances_df[criterion].apply(
            lambda x: (max(ideal_distances_df[criterion]) - x)
        )
        anti_ideal_distances_df[criterion] = anti_ideal_distances_df[criterion].apply(
            lambda x: (x - min(anti_ideal_distances_df[criterion]))
        )

    return (ideal_distances_df, anti_ideal_distances_df)


def compute_similarity(
    ideal_distances_df: pd.DataFrame,
    anti_ideal_distances_df: pd.DataFrame,
    weights: dict[str, Criterion],
):
    """
    Return a dataframe with the similarity of each solution to the ideal and anti-ideal solutions
    """
    similarity_df: pd.DataFrame = pd.DataFrame(columns=["criterion", "similarity"])

    names: pd.Series = ideal_distances_df[list(ideal_distances_df.columns)[0]]

    for i in range(len(ideal_distances_df)):
        ideal = 0
        anti_ideal = 0
        for criterion in weights.keys():
            ideal += ideal_distances_df.loc[i][criterion]
            anti_ideal += anti_ideal_distances_df.loc[i][criterion]
        similarity = round(anti_ideal / (ideal + anti_ideal), 4)
        similarity_df.loc[i] = [names[i], similarity]

    # Order the dataframe by similarity
    similarity_df.sort_values(by="similarity", ascending=True, inplace=True)

    return similarity_df


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
    (ideal_distances, anti_ideal_distances_df) = compute_distances(
        normalized_solutions, weights
    )
    similarity_df: pd.DataFrame = compute_similarity(
        ideal_distances, anti_ideal_distances_df, weights
    )

    similarity_df.to_csv(output_path + "topsis_solutions.csv", index=False)
