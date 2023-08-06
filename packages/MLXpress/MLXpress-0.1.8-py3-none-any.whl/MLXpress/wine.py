from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

wine = load_wine()
X = wine.data
y = wine.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=12)


def classification(model, x=None, y=None):
    """
      Perform classification using the specified model and calculate accuracy.

      Parameters:
      - model: The classification model.
      - x: The input data. If None, it uses X_test.
      - y: The target labels. If None, it uses y_test.

      Returns:
      - ac1: The accuracy of the model as a string.
      """
    if x is None:
        x = X_test
    if y is None:
        y = y_test
    model.fit(X_train, y_train)
    y_pred = model.predict(x)
    cm = confusion_matrix(y, y_pred)
    fig = plt.figure(num="Confusion Matrix")
    sns.heatmap(cm, annot=True, cmap='Blues')

    plt.show()
    ac = accuracy_score(y_test, y_pred)
    ac1 = f"The accuracy of the model is {ac * 100:.2f} % and the other metrics are as follows:\n"
    print(ac1)
    cr = classification_report(y_test, y_pred)
    print(cr)
    return ac1


def predict(model, x):
    """
        Perform prediction using the specified model.

        Parameters:
        - model: The trained model.
        - x: The input data for prediction.

        Returns:
        - pred1: The prediction result as a string.

        """

    pred = model.predict(x)
    pred1 = f"The instance belongs to class {pred}"
    print(pred1)
    return pred1


def vis(model, X=X_test, y=y_test):
    """
    Visualize box plots for each feature based on the target variable.

    Parameters:
    - model: The model used for visualization.
    - X: The input data. Defaults to X_test.
    - y: The target variable. Defaults to y_test.
    """

    wine1 = load_wine()
    df = pd.DataFrame(X, columns=wine1.feature_names)
    df['Target'] = wine1.target_names[y]

    num_features = len(wine1.feature_names)
    num_rows = (num_features - 1) // 2 + 1
    num_cols = min(2, num_features)

    # Create subplots based on the number of features
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 8))

    for i, feature in enumerate(wine1.feature_names):
        row = i // num_cols
        col = i % num_cols
        sns.boxplot(x='Target', y=feature, data=df, ax=axes[row, col])

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Set the title of the figure
    plt.suptitle('Box Plot')
    plt.show()
