def recall(true_positive, false_negative):
    """
    Calculate recall.

    Recall = TP / (TP + FN)
    """

    denominator = true_positive + false_negative

    if denominator == 0:
        return 0.0

    return true_positive / denominator