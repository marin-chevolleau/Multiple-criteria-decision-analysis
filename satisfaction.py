import pandas as pd

from criterion import Criterion

def is_dominated(row: pd.Series, criteria: dict[str, Criterion]) -> bool:
    """
    Return True if the row is dominated by at least one satisfaction treshold from the criteria
    """
    for criterion, descriptors in criteria.items():
        if descriptors.veto != 0 and abs(row[criterion] - descriptors.satisfaction) > descriptors.veto:
            return False
        if descriptors.direction == "maximize" and row[criterion] + descriptors.indifference < descriptors.satisfaction:
            return True
        elif descriptors.direction == "minimize" and row[criterion] - descriptors.indifference > descriptors.satisfaction:
            return True

    return False


def retrieve_satisfying_solutions(df: pd.DataFrame, criteria: dict[str, Criterion]) -> pd.DataFrame:
    """
    Return the subset of solutions satisfying the criteria
    """
    return df[~df.apply(is_dominated, axis=1, criteria=criteria)]


if __name__ == "__main__":
    input_path = "data/"
    output_path = "output/"
    
    initial_solutions: pd.DataFrame = pd.read_csv(input_path + "data.csv")
    satisfaction: dict = {
        "C1": Criterion("minimize", 50000, 0, 5000000),
        "C2": Criterion("minimize", 0, 0, 10000),
        "C3": Criterion("maximize", 0, 0, 60),
        "C4": Criterion("minimize", 30, 0, 75),
        "C5": Criterion("minimize", 0, 0, 50),
        "C6": Criterion("maximize", 1, 0, 4),
        "C7": Criterion("maximize", 0, 2, 2),
    }

    preanalysed_solutions: pd.DataFrame = retrieve_satisfying_solutions(
        initial_solutions, satisfaction
    )

    preanalysed_solutions.to_csv(output_path + "preanalysed_solutions_satisfaction.csv", index=False)
