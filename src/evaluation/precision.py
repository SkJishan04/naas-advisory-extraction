def precision(true_positive, false_positive):
    """
    Calculate precision.

    Precision = TP / (TP + FP)
    """

    denominator = true_positive + false_positive

    if denominator == 0:
        return 0.0

    return true_positive / denominator