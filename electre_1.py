import pandas as pd
from typing import Union

import networkx as nx
import matplotlib.pyplot as plt

def normalize(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return a normalized version of a dataframe
    """
    normalized_df: pd.DataFrame = df.copy()
    
    # Reorder minimizing criteria
    for criterion, descriptors in criteria.items():
        if descriptors[0] == "minimize":
            normalized_df[criterion] = normalized_df[criterion].apply(lambda x: (max(df[criterion]) - x))
    
    # Normalize veto and indifference thresholds
    for criterion, descriptors in criteria.items():
        if descriptors[1] != 0: descriptors[1] = (descriptors[1] / (max(normalized_df[criterion]) - min(normalized_df[criterion])))
        if descriptors[2] != 0: descriptors[2] = (descriptors[2] / (max(normalized_df[criterion]) - min(normalized_df[criterion])))
    
    # Normalize criteria and multiply them by their weight
    for criterion in criteria.keys():
        normalized_df[criterion] = normalized_df[criterion].apply(lambda x: 
            ((x - min(normalized_df[criterion])) / (max(normalized_df[criterion]) - min(normalized_df[criterion]))))
    
    return normalized_df

def concordance(row1: pd.Series, row2: pd.Series, criteria: dict) -> Union[None, float]:
    """
    Return the concordance of the two rows
    """
    concordance: Union[None, float] = 0
    
    for criterion, descriptors in criteria.items():
        indifference: float = descriptors[1]
        veto: float = descriptors[2]
        weight: float = descriptors[3]
        
        if veto != 0 and abs(row1[criterion] - row2[criterion]) > veto: return None
        if (row1[criterion] + indifference) >= row2[criterion]: concordance += weight
            
    return concordance


def concordance_matrix(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return the concordance matrix of the dataframe
    """
    concordance_matrix: pd.DataFrame = pd.DataFrame(index=df.index, columns=df.index)
    
    for i in range(len(df)):
        for j in range(len(df)):
            if i == j: concordance_matrix.loc[i, j] = None
            else: concordance_matrix.loc[i, j] = concordance(df.loc[i], df.loc[j], criteria)
            
    return concordance_matrix


def discordance(row1: pd.Series, row2: pd.Series, criteria: dict) -> Union[None, float]:
    """
    Return the discordance of the two rows
    """
    
    observed_discordances: list = []
    
    for criterion, descriptors in criteria.items():
        indifference: float = descriptors[1]
        veto: float = descriptors[2]
        
        if veto != 0 and abs(row1[criterion] - row2[criterion]) > veto: return None

        if (row1[criterion] + indifference) < row2[criterion]: observed_discordances.append(abs(row2[criterion] - (row1[criterion])))
        else: observed_discordances.append(0)
            
    return max(observed_discordances)


def discordance_matrix(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Return the discordance matrix of the dataframe
    """
    discordance_matrix: pd.DataFrame = pd.DataFrame(index=df.index, columns=df.index)
    
    for i in range(len(df)):
        for j in range(len(df)):
            if i == j: discordance_matrix.loc[i, j] = None
            else: discordance_matrix.loc[i, j] = discordance(df.loc[i], df.loc[j], criteria)
            
    return discordance_matrix


def treshold_matrix(concordance_matrix: pd.DataFrame, discordance_matrix: pd.DataFrame, 
                    concordance_treshold: float, discordance_treshold: float, criteria: dict) -> pd.DataFrame:
    """
    Return the matrix of relations respecting the tresholds
    """
    treshold_matrix: pd.DataFrame = pd.DataFrame(index=concordance_matrix.index, columns=concordance_matrix.columns)
    
    # Multiply concordance treshold by the sum of the weights (to have the same scale as the concordance matrix)
    concordance_treshold *= sum([descriptors[3] for descriptors in criteria.values()])
    # Multiply the discordance treshold by the maximum discordance in the discordance matrix (to have the same scale as the discordance matrix)
    discordance_treshold *= discordance_matrix.max().max()
    
    for i in range(len(concordance_matrix)):
        for j in range(len(concordance_matrix)):
            if i == j: treshold_matrix.loc[i, j] = None
            else:
                if concordance_matrix.loc[i, j] is None: treshold_matrix.loc[i, j] = None
                elif (concordance_matrix.loc[i, j] >= concordance_treshold and
                      discordance_matrix.loc[i, j] <= discordance_treshold): treshold_matrix.loc[i, j] = True
                else: treshold_matrix.loc[i, j] = False
                
    return treshold_matrix


def visualize_matrix(matrix: pd.DataFrame):
    """
    Visualize the matrix as a graph
    """
    G = nx.DiGraph()

    for node in matrix.index:
        G.add_node(node)
        
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix.iloc[i, j] is True:
                G.add_edge(i, j)

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)

    plt.show()


if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("preanalysed_solutions.csv")
    # {criterion: [Direction, Indifference, Veto, Weight]}
    criteria: dict = {"C1": ["minimize", 50000, 0, 1], "C2": ["minimize", 0, 0, 2], "C3": ["maximize", 0, 0, 4],
                       "C4": ["minimize", 30, 0, 5], "C5": ["minimize", 0, 0, 3], "C6": ["maximize", 1, 0, 5], 
                       "C7": ["maximize", 0, 2, 4]}
    
    # Retrieve the normalized solutions and new indifference and veto thresholds
    normalized_solutions: pd.DataFrame = normalize(initial_solutions, criteria)
    
    concordance_treshold: float = 0.95
    discordance_treshold: float = 0.6
    
    concordance_matrix: pd.DataFrame = concordance_matrix(normalized_solutions, criteria)
    discordance_matrix: pd.DataFrame = discordance_matrix(normalized_solutions, criteria)
    treshold_matrix: pd.DataFrame = treshold_matrix(concordance_matrix, discordance_matrix, concordance_treshold, discordance_treshold, criteria)
    
    visualize_matrix(treshold_matrix)