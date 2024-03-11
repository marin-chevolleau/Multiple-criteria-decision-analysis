import pandas as pd

from criterion import Criterion

def is_dominated(row: pd.Series, df: pd.DataFrame, criteria: dict[str, Criterion]) -> bool:
    """
    Return True if the row is dominated by at least one row in the dataframe
    """
    for i in range(len(df)):
        # Do not compare the row with itself
        if (df.iloc[i] == row).all():
            continue

        other_row: pd.Series = df.iloc[i]
        for criterion, descriptors in criteria.items():
            if descriptors.veto != 0 and abs(row[criterion] - other_row[criterion]) > descriptors.veto:
                return False
            if (
                descriptors.direction == "maximize"
                and row[criterion] + descriptors.indifference < other_row[criterion]
            ):
                return True
            elif (
                descriptors.direction == "minimize"
                and row[criterion] - descriptors.indifference > other_row[criterion]
            ):
                return True

    return False


def retrieve_pareto_front(df: pd.DataFrame, criteria: dict[str, Criterion]) -> pd.DataFrame:
    """
    Return the Pareto front, i.e. the subset of non-dominated solutions
    """
    return df[~df.apply(is_dominated, axis=1, df=df, criteria=criteria)]


if __name__ == "__main__":
    input_path = "data/"
    output_path = "output/"

    initial_solutions: pd.DataFrame = pd.read_csv(
        input_path + "data.csv"
    )
    
    criteria: dict = {"C4": Criterion("minimize", 30, 0), "C6": Criterion("maximize", 1, 0)}

    preanalysed_solutions: pd.DataFrame = retrieve_pareto_front(
        initial_solutions, criteria
    )

    preanalysed_solutions.to_csv(output_path + "preanalysed_solutions_dominance.csv", index=False)
