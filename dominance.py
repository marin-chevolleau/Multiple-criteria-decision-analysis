import pandas as pd

def is_dominated(row: pd.Series, df: pd.DataFrame, critera: dict) -> bool:
    """
    Return True if the row is dominated by at least one row in the dataframe
    """
    for i in range(len(df)):
        # Do not compare the row with itself
        if (df.iloc[i] == row).all():
            continue
        
        other_row: pd.Series = df.iloc[i]
        for criterion, descriptors in critera.items():
            direction: str = descriptors[0]
            indifference: float = descriptors[1]
            veto: float = descriptors[2]
            if veto != 0 and abs(row[criterion] - other_row[criterion]) > veto: return False
            if direction == "maximize" and row[criterion] + indifference < other_row[criterion]: return True
            elif direction == "minimize" and row[criterion] - indifference > other_row[criterion]: return True 
            
    return False


def retrieve_pareto_front(df: pd.DataFrame, critera: dict) -> pd.DataFrame:
    """
    Return the Pareto front, i.e. the subset of non-dominated solutions
    """
    return df[~df.apply(is_dominated, axis=1, df=df, critera=critera)]


if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("initial_solutions.csv")
    # {criterion: [Direction, Indifference, Veto]}
    criteria:dict = {"C4": ["minimize", 30, 0], "C6": ["maximize", 1, 0]}
    
    preanalysed_solutions: pd.DataFrame = retrieve_pareto_front(initial_solutions, criteria)
    
    preanalysed_solutions.to_csv("preanalysed_solutions.csv", index=False)
    
    
    
    