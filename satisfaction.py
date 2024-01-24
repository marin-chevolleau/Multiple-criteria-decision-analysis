import pandas as pd

def is_dominated(row: pd.Series, criteria: dict) -> bool:
    """
    Return True if the row is dominated by at least one satisfaction treshold from the criteria
    """
    for criterion, descriptors in criteria.items():
        direction: str = descriptors[0]
        indifference: float = descriptors[1]
        veto: float = descriptors[2]
        satisfaction: float = descriptors[3]
        if veto != 0 and abs(row[criterion] - satisfaction) > veto: return False
        if direction == "maximize" and row[criterion] + indifference < satisfaction: return True
        elif direction == "minimize" and row[criterion] - indifference > satisfaction: return True 
        
    return False


def retrieve_satisfying_solutions(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return the subset of solutions satisfying the criteria
    """
    return df[~df.apply(is_dominated, axis=1, criteria=criteria)]


if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("initial_solutions.csv")
    # {criterion: [Direction, Indifference, Veto, Satisfaction]}
    satisfaction: dict = {"C1": ["minimize", 50000, 0, 5000000], "C2": ["minimize", 0, 0, 10000], 
                          "C3": ["maximize", 0, 0, 60], "C4": ["minimize", 30, 0, 75], 
                          "C5": ["minimize", 0, 0, 50], "C6": ["maximize", 1, 0, 4], 
                          "C7": ["maximize", 0, 2, 2]}
    
    preanalysed_solutions: pd.DataFrame =  retrieve_satisfying_solutions(initial_solutions, satisfaction)
    
    preanalysed_solutions.to_csv("preanalysed_solutions.csv", index=False)