import pandas as pd

from satisfaction import *
from dominance import *

from topsis import *
from weighting import *

from electre_1 import *

if __name__ == "__main__":
    input_path = "data/"
    output_path = "output/"

    initial_solutions: pd.DataFrame = pd.read_csv(input_path + "data.csv")
    criteria: dict = {
        "C1": Criterion("minimize", 50000, 0, 5000000, weight=1),
        "C2": Criterion("minimize", 0, 0, 10000, weight=2),
        "C3": Criterion("maximize", 0, 0, 60, weight=4),
        "C4": Criterion("minimize", 30, 0, 75, weight=3),
        "C5": Criterion("minimize", 0, 0, 50, weight=3),
        "C6": Criterion("maximize", 1, 0, 4, weight=5),
        "C7": Criterion("maximize", 0, 2, 2, weight=3),
    }

    # Satisfaction
    preanalysed_solutions_satisfaction: pd.DataFrame = retrieve_satisfying_solutions(
        initial_solutions, criteria
    )

    # Save the preanalysed solutions
    preanalysed_solutions_satisfaction.to_csv(
        output_path + "preanalysed_solutions_satisfaction.csv", index=False
    )

    # Dominance
    initial_solutions: pd.DataFrame = pd.read_csv(input_path + "data.csv")

    dominance_criteria: dict = {
        "C4": Criterion("minimize", 30, 0),
        "C6": Criterion("maximize", 1, 0),
    }

    preanalysed_solutions_dominance: pd.DataFrame = retrieve_pareto_front(
        initial_solutions, dominance_criteria
    )

    # Save the preanalysed solutions
    preanalysed_solutions_dominance.to_csv(
        output_path + "preanalysed_solutions_dominance.csv", index=False
    )

    # Choose the preanalysed solutions for the following processes
    preanalysed_solutions = preanalysed_solutions_dominance
    # preanalysed_solutions = preanalysed_solutions_satisfaction
    
    # reindex dataframe
    preanalysed_solutions = preanalysed_solutions.reset_index(drop=True)
    
    # Topsis
    normalized_solutions: pd.DataFrame = normalize(preanalysed_solutions, criteria)

    (ideal_distances, anti_ideal_distances_df) = compute_distances(
        normalized_solutions, criteria
    )

    similarity_df: pd.DataFrame = compute_similarity(
        ideal_distances, anti_ideal_distances_df, criteria
    )

    similarity_df.to_csv(output_path + "topsis_solutions.csv", index=False)

    # Weighting
    normalized_solutions: pd.DataFrame = normalize(preanalysed_solutions, criteria)
    weighted_solutions: pd.DataFrame = compute_weights(normalized_solutions, criteria)

    weighted_solutions.to_csv(output_path + "weighted_solutions.csv", index=False)

    # Electre 1
    normalized_solutions: pd.DataFrame = normalize(initial_solutions, criteria)
    criteria = normalize_criteria(normalized_solutions, criteria)

    concordance_treshold: float = 0.95
    discordance_treshold: float = 0.6

    concordance_matrix: pd.DataFrame = get_concordance_matrix(
        normalized_solutions, criteria
    )
    discordance_matrix: pd.DataFrame = get_discordance_matrix(
        normalized_solutions, criteria
    )
    treshold_matrix: pd.DataFrame = get_treshold_matrix(
        concordance_matrix,
        discordance_matrix,
        concordance_treshold,
        discordance_treshold,
        criteria,
    )

    visualize_matrix(treshold_matrix)
