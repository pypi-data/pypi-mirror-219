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
    ac1 = f"The accuracy of the model is {ac * 100:.2f} %"
    return ac1


def predict(model, x):
    pred = model.predict(x)
    pred1 = f"The instance belongs to class {pred}"
    return pred1


def vis(model, X=X_test, y=y_test):
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
    model.fit(X)
    labels = model.labels_
    silhouette = silhouette_score(X, labels)

    print("Cluster Labels:")
    for sample_idx, label in enumerate(labels):
        print(f"Sample {sample_idx + 1}: Cluster {label}")

    print("Silhouette Score:", silhouette)
    return labels





def vis_clusters(model):
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
