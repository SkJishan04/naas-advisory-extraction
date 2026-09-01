def accuracy(true_positive, true_negative, false_positive, false_negative):
    """
    Calculate classification accuracy.
    """

    denominator = (
        true_positive
        + true_negative
        + false_positive
        + false_negative
    )

    if denominator == 0:
        return 0.0

    return (
        true_positive + true_negative
    ) / denominator