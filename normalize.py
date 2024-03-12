import pandas as pd

from criterion import Criterion

def normalize(df: pd.DataFrame, criteria: dict[str, Criterion], use_weight: bool = False) -> pd.DataFrame:
    """
    Return a normalized version of a dataframe
    """
    normalized_df: pd.DataFrame = df.copy()

    for criterion, descriptors in criteria.items():
        # Reorder minimizing criteria
        if descriptors.direction == "minimize":
            normalized_df[criterion] = normalized_df[criterion].apply(
                lambda x: (max(normalized_df[criterion]) - x)
            )

        # Normalize criteria and multiply
        normalized_df[criterion] = normalized_df[criterion].apply(
            lambda x: (
                (x - min(normalized_df[criterion]))
                / (max(normalized_df[criterion]) - min(normalized_df[criterion]))
            )
        )
        
        # Multiply each criterion by its weight
        if use_weight:
            normalized_df[criterion] = normalized_df[criterion] * descriptors.weight

    return normalized_df

def normalize_criteria(normalized_df: pd.DataFrame, criteria: dict[str, Criterion]):
    # Normalize veto and indifference thresholds
    for criterion, descriptors in criteria.items():
        if descriptors.indifference != 0:
            descriptors.indifference = descriptors.indifference / (
                max(normalized_df[criterion]) - min(normalized_df[criterion])
            )
        if descriptors.veto != 0:
            descriptors.veto = descriptors.veto / (
                max(normalized_df[criterion]) - min(normalized_df[criterion])
            )
    
    return criteria