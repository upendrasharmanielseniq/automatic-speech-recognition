from sklearn.metrics import classification_report

def multiclass_classification_report(targets, predictions):
    """
    Generates a classification report using scikit-learn.

    Parameters:
    - target: list or array-like of true labels
    - predictions: list or array-like of predicted labels

    Returns:
    - A string containing the classification report
    """
    report = classification_report(targets, predictions)
    print("Classification Report:\n")
    print(report)
    return report