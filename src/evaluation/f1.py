def f1_score(precision_value, recall_value):
    """
    Calculate F1-score.
    """

    denominator = precision_value + recall_value

    if denominator == 0:
        return 0.0

    return (
        2 * precision_value * recall_value
        / denominator
    )