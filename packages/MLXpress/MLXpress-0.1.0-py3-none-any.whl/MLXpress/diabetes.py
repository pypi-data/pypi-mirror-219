from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

d = load_diabetes()
X = d.data
y = d.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=12)


def regression(model, x=None, y=None):
    if x is None:
        x = X_test
    if y is None:
        y = y_test
    model.fit(X_train, y_train)
    y_pred = model.predict(x)
    mse = mean_squared_error(y_test, y_pred)
    MSE = f"The MSE of the model is {mse:.2f} "
    return MSE


def predict(model, x):
    pred = model.predict(x)
    pred1 = f"Predicted Disease Progression: {pred}"
    return pred1


def vis(model, X=X_test, y=y_test):
    diabetes = load_diabetes()
    df = pd.DataFrame(X, columns=diabetes.feature_names)
    df['Target'] = y

    num_features = len(diabetes.feature_names)
    num_rows = (num_features - 1) // 2 + 1
    num_cols = min(2, num_features)

    # Create subplots based on the number of features
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 8))

    for i, feature in enumerate(diabetes.feature_names):
        row = i // num_cols
        col = i % num_cols
        sns.regplot(x=feature, y='Target', data=df, ax=axes[row, col])

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Set the title of the figure
    plt.suptitle('Regression Analysis for Diabetes')

    plt.show()
