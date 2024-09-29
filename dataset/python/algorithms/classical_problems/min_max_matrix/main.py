def min_path_matrix(weights):
    right_border = len(weights[0]) - 1
    bottom_border = len(weights) - 1
    dp_weights = [weight[:] for weight in weights]

    for i in range(1, len(weights)):
        dp_weights[i][0] += dp_weights[i - 1][0]

    for i in range(1, len(weights[0])):
        dp_weights[0][i] += dp_weights[0][i - 1]

    for i in range(1, len(weights)):
        for j in range(1, len(weights[0])):
            dp_weights[i][j] = weights[i][j] + min(
                dp_weights[i - 1][j], dp_weights[i][j - 1]
            )
    return dp_weights[bottom_border][right_border]
