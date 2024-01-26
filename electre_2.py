import pandas as pd
from typing import Union


def concordance(row1: pd.Series, row2: pd.Series, criteria: dict) -> Union[None, float]:
    """
    Return the concordance of the two rows
    """
    concordance: Union[None, float] = 0
    
    for criterion, descriptors in criteria.items():
        direction: str = descriptors[0]
        indifference: float = descriptors[1]
        veto: float = descriptors[2]
        weight: float = descriptors[3]
        
        if veto != 0 and abs(row1[criterion] - row2[criterion]) > veto: return None
        if direction == "maximize":
            if (row1[criterion] + indifference) >= row2[criterion]: concordance += weight
        elif direction == "minimize":
            if (row1[criterion] - indifference) <= row2[criterion]: concordance += weight
            
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
        direction: str = descriptors[0]
        indifference: float = descriptors[1]
        veto: float = descriptors[2]
        
        if veto != 0 and abs(row1[criterion] - row2[criterion]) > veto: return None
        if direction == "maximize":
            if (row1[criterion] + indifference) < row2[criterion]: observed_discordances.append(abs(row2[criterion] - (row1[criterion])))
            else: observed_discordances.append(0)
        elif direction == "minimize":
            if (row1[criterion] - indifference) > row2[criterion]: observed_discordances.append(abs(row2[criterion] - (row1[criterion])))
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


def obstructive_free_matrix(concordance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Return a version of the concordance matrix free from obstructive cycles
    """
    obstructive_free_matrix: pd.DataFrame = concordance_matrix.copy()
    
    # Remove solutions that may be obstructive (P+,P=) < (P-,P=)
    for i in range(len(obstructive_free_matrix)):
        for j in range(len(obstructive_free_matrix)):
            if obstructive_free_matrix.loc[i, j] is None:
                continue
            if obstructive_free_matrix.loc[j, i] is None:
                continue
            if obstructive_free_matrix.loc[i, j] < obstructive_free_matrix.loc[j, i]:
                obstructive_free_matrix.loc[i, j] = None
                obstructive_free_matrix.loc[j, i] = None
    
    return obstructive_free_matrix
    

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


def high_dominance_matrix(df: pd.DataFrame, criteria: dict, tresholds: tuple) -> pd.DataFrame:
    """
    Return the high dominance matrix of the dataframe
    """
    (c_plus, c_0, _, d_1, d_2) = tresholds
    
    # Obtain the concordance and discordance matrices
    concordance: pd.DataFrame = obstructive_free_matrix(concordance_matrix(df, criteria))
    discordance: pd.DataFrame = discordance_matrix(df, criteria)
    
    # Obtain the high and medium dominance matrices
    high_dominance_matrix: pd.DataFrame = treshold_matrix(concordance, discordance, c_plus, d_1, criteria)
    medium_dominance_matrix: pd.DataFrame = treshold_matrix(concordance, discordance, c_0, d_2, criteria)
    
    # Obtain the final high dominance matrix by setting the values of the medium dominance matrix where the high dominance matrix is None
    high_dominance_matrix = high_dominance_matrix.where(high_dominance_matrix.isnull(), medium_dominance_matrix)
    
    return high_dominance_matrix


def low_dominance_matrix(df: pd.DataFrame, criteria: dict, tresholds: tuple) -> pd.DataFrame:
    """
    Return the low dominance matrix of the dataframe
    """
    (_, _, c_minus, d_1, _) = tresholds
    
    # Obtain the concordance and discordance matrices
    concordance: pd.DataFrame = obstructive_free_matrix(concordance_matrix(df, criteria))
    discordance: pd.DataFrame = discordance_matrix(df, criteria)
    
    # Obtain the low dominance matrix
    low_dominance_matrix: pd.DataFrame = treshold_matrix(concordance, discordance, c_minus, d_1, criteria)
    
    return low_dominance_matrix


def exploit_dominance(high_dominance_matrix: pd.DataFrame, low_dominance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Return the dominance matrix obtained by exploiting the high and low dominance matrices
    """
    solutions_to_rank: list = list(range(len(high_dominance_matrix)))
    ranked_solutions: list = []
    
    while len(solutions_to_rank) > 0:
        
        # Actions that are not dominated in the high dominance matrix (no True in their column)
        D: list = [action for action in solutions_to_rank if not high_dominance_matrix.loc[action, solutions_to_rank].any()]
        # Actions from D linked between them in the low dominance matrix
        U: list = [action for action in D if low_dominance_matrix.loc[action, D].any()]
        # Actions from U that are not dominated in the low dominance matrix (no True in their column)
        B: list = [action for action in U if not low_dominance_matrix.loc[action, U].any()]
        
        # Best actions are {D \ U} union {B}
        best_actions: list = list(set(D).difference(U).union(B))
        
        ranked_solutions.append(best_actions)
        solutions_to_rank = list(set(solutions_to_rank).difference(best_actions))
    
    return ranked_solutions


def ranked_solutions_name(ranked_solutions: list, df: pd.DataFrame, name_column: int) -> list:
    """
    Return the ranked solutions with their names
    """
    ranked_solutions_names: list = []
    
    for solution in ranked_solutions:
        ranked_solutions_names.append(list(df.loc[solution, df.columns[name_column]]))
        
    return ranked_solutions_names


if __name__ == "__main__":
    initial_solutions: pd.DataFrame = pd.read_csv("preanalysed_solutions.csv")
    # {criterion: [Direction, Indifference, Veto, Weight]}
    criteria: dict = {"C1": ["minimize", 50000, 0, 1], "C2": ["minimize", 0, 0, 2], "C3": ["maximize", 0, 0, 4],
                       "C4": ["minimize", 30, 0, 5], "C5": ["minimize", 0, 0, 3], "C6": ["maximize", 1, 0, 5], 
                       "C7": ["maximize", 0, 2, 4]}
    # [High concordance treshold, Medium concordance treshold, Low concordance treshold, High discordance treshold, Low discordance treshold]
    tresholds: tuple = (0.95, 0.6, 0.3, 0.6, 0.3)
    
    high_dominance: pd.DataFrame = high_dominance_matrix(initial_solutions, criteria, tresholds)
    low_dominance: pd.DataFrame = low_dominance_matrix(initial_solutions, criteria, tresholds)
    
    ranked_solutions: list = exploit_dominance(high_dominance, low_dominance)
    ranked_solutions_names: list = ranked_solutions_name(ranked_solutions, initial_solutions, 0)

    print(ranked_solutions_names)