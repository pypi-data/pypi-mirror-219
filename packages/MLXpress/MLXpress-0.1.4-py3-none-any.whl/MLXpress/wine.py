from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
wine = load_wine()
X = wine.data
y = wine.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=12)


def classification(model,x=None, y=None):
    if x is None:
        x = X_test
    if y is None:
        y = y_test
    model.fit(X_train, y_train)
    y_pred = model.predict(x)
    cm = confusion_matrix(y, y_pred)
    sns.heatmap(cm,annot=True,cmap='Blues')
    plt.show()
    ac = accuracy_score(y_test, y_pred)
    ac1= f"The accuracy of the model is {ac*100:.2f} %"
    return ac1
def predict(model,x):
    pred=model.predict(x)
    pred1=f"The instance belongs to class {pred}"
    return pred1


