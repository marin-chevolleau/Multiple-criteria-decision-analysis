import pandas as pd

def normalize(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return a normalized version of a dataframe
    """
    normalized_df: pd.DataFrame = df.copy()
    
    # Reorder minimizing criteria
    for criterion, descriptors in criteria.items():
        if descriptors[0] == "minimize":
            normalized_df[criterion] = normalized_df[criterion].apply(lambda x: (max(normalized_df[criterion]) - x) * descriptors[1])
            
    # Normalize criteria and multiply them by their weight
    for criterion in criteria.keys():
        normalized_df[criterion] = normalized_df[criterion].apply(lambda x: 
            ((x - min(normalized_df[criterion])) / (max(normalized_df[criterion]) - min(normalized_df[criterion]))) * criteria[criterion][1])
    
    return normalized_df


def compute_distances(df: pd.DataFrame, criteria: dict):
    """
    Return a dataframe with the distances to the ideal and anti-ideal solutions appended
    """
    ideal_distances_df: pd.DataFrame = df.copy()
    anti_ideal_distances_df: pd.DataFrame = df.copy()
    
    for criterion in criteria.keys():
        ideal_distances_df[criterion] = ideal_distances_df[criterion].apply(lambda x: (max(ideal_distances_df[criterion]) - x))
        anti_ideal_distances_df[criterion] = anti_ideal_distances_df[criterion].apply(lambda x: (x - min(anti_ideal_distances_df[criterion])))
    
    return (ideal_distances_df, anti_ideal_distances_df)


def compute_similarity(ideal_distances_df: pd.DataFrame, anti_ideal_distances_df: pd.DataFrame, criteria: dict):
    """
    Return a dataframe with the similarity of each solution to the ideal and anti-ideal solutions
    """
    similarity_df: pd.DataFrame = pd.DataFrame(columns=["criterion", "similarity"])
    
    # Retrieve the names as the only column of the dataframe not in criteria
    names: pd.Series = ideal_distances_df[list(set(ideal_distances_df.columns) - set(criteria.keys()))[0]]
    
    for i in range(len(ideal_distances_df)):
        ideal = 0
        anti_ideal = 0
        for criterion in criteria.keys():
            ideal += ideal_distances_df.loc[i][criterion]
            anti_ideal += anti_ideal_distances_df.loc[i][criterion]
        similarty = round(anti_ideal / (ideal + anti_ideal), 4)
        similarity_df.loc[i] = [names[i], similarty]
        
    # Order the dataframe by similarity
    similarity_df.sort_values(by="similarity", ascending=True, inplace=True)
        
    return similarity_df    


if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("preanalysed_solutions.csv")
    # {criterion: [Direction, Weight]}
    criteria: dict = {"C1": ["minimize", 1], "C2": ["minimize", 2], "C3": ["maximize", 4],
                      "C4": ["minimize", 5], "C5": ["minimize", 3], "C6": ["maximize", 5], 
                      "C7": ["maximize", 4]}

    normalized_solutions: pd.DataFrame = normalize(initial_solutions, criteria)
    (ideal_distances, anti_ideal_distances_df) = compute_distances(normalized_solutions, criteria)
    similarity_df: pd.DataFrame = compute_similarity(ideal_distances, anti_ideal_distances_df, criteria)
    
    similarity_df.to_csv("topsis_solutions.csv", index=False)
    
    