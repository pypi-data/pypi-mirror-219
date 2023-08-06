from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import silhouette_score
import numpy as np
iris = load_iris()
X = iris.data
y = iris.target
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
    cr=classification_report(y_test, y_pred)
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

    iris = load_iris()
    df = pd.DataFrame(X, columns=iris.feature_names)
    df['Target'] = iris.target_names[y]
    # Create a box plot for each feature
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for i, feature in enumerate(iris.feature_names):
        row = i // 2
        col = i % 2
        sns.boxplot(x='Target', y=feature, data=df, ax=axes[row, col])

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Set the title of the figure
    plt.suptitle('Box Plot')
    plt.show()


def clustering(model, num_clusters):
    """
       Perform clustering using the specified model and calculate silhouette score.

       Parameters:
       - model: The clustering model.
       - num_clusters: The number of clusters to create.

       Returns:
       - labels: The cluster labels as an array.

       """
    model.fit(X)
    labels = model.labels_
    silhouette = silhouette_score(X, labels)

    print("Cluster Labels:")
    for sample_idx, label in enumerate(labels):
        print(f"Sample {sample_idx + 1}: Cluster {label}")

    print("Silhouette Score:", silhouette)
    return labels





def vis_clusters(model):
    """
       Visualize the clustering results.

       Parameters:
       - model: The clustering model.

       """
    features = globals().get('X')

    if features is None:
        raise ValueError("Features must be set as a global variable.")

    labels = model.labels_

    unique_labels = np.unique(labels)

    fig, ax = plt.subplots(figsize=(8, 6))

    for label in unique_labels:
        cluster_samples = features[labels == label]
        ax.scatter(cluster_samples[:, 0], cluster_samples[:, 1], label=f"Cluster {label}")

    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title("Clustering Results")
    ax.legend()

    plt.show()
