import pandas as pd

def normalize(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return a normalized version of a dataframe
    """
    normalized_df: pd.DataFrame = df.copy()
    
    # Reorder minimizing criteria
    for criterion, descriptors in criteria.items():
        if descriptors[0] == "minimize":
            normalized_df[criterion] = normalized_df[criterion].apply(lambda x: max(df[criterion]) - x)
            
    # Normalize criteria values between 0 and 1
    for criterion in criteria.keys():
        normalized_df[criterion] = normalized_df[criterion].apply(lambda x: 
            (x - min(df[criterion])) / (max(df[criterion]) - min(df[criterion])))
    
    return normalized_df
    
    
def compute_weights(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return a dataframe with a column containing the weighted sum of the criteria
    """
    weighted_df: pd.DataFrame = df.copy()
    
    # Multiply each criterion by its weight and sum the results
    for criterion, descriptors in criteria.items():
        weighted_df[criterion] = weighted_df[criterion] * descriptors[1]
    
    # Create a new column for the weighted sum with 4 decimals
    weighted_df["Weighted sum"] = weighted_df[list(criteria.keys())].sum(axis=1).round(4)
    
    # Drop the criterion columns
    weighted_df = weighted_df.drop(columns=list(criteria.keys()))
    
    # Order the dataframe by the weighted sum
    weighted_df = weighted_df.sort_values(by="Weighted sum")
    
    return weighted_df
    

if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("preanalysed_solutions.csv")
    # {criterion: [Direction, Weight]}
    criteria: dict = {"C1": ["minimize", 1], "C2": ["minimize", 2], "C3": ["maximize", 4],
                       "C4": ["minimize", 1], "C5": ["minimize", 3], "C6": ["maximize", 5], 
                       "C7": ["maximize", 4]}
    
    normalized_solutions: pd.DataFrame = normalize(initial_solutions, criteria)
    weighted_solutions: pd.DataFrame = compute_weights(normalized_solutions, criteria)
    
    weighted_solutions.to_csv("weighted_solutions.csv", index=False)