def evaluate_model(model, X_test, y_test):
    """
    Evaluate the performance of a machine learning model.

    Parameters:
    model: The trained machine learning model to evaluate.
    X_test: The test features.
    y_test: The true labels for the test set.

    Returns:
    dict: A dictionary containing evaluation metrics.
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    y_pred = model.predict(X_test)

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }

    return metrics


def cross_validate(model, X, y, cv=5):
    """
    Perform cross-validation on a machine learning model.

    Parameters:
    model: The machine learning model to validate.
    X: The features.
    y: The labels.
    cv: The number of cross-validation folds.

    Returns:
    list: A list of evaluation scores for each fold.
    """
    from sklearn.model_selection import cross_val_score

    scores = cross_val_score(model, X, y, cv=cv)

    return scores.tolist()


def plot_metrics(metrics):
    """
    Plot evaluation metrics.

    Parameters:
    metrics: A dictionary containing evaluation metrics.
    """
    import matplotlib.pyplot as plt

    labels = list(metrics.keys())
    values = list(metrics.values())

    plt.bar(labels, values)
    plt.ylabel('Score')
    plt.title('Model Evaluation Metrics')
    plt.show()