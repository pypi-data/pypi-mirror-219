from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
def handle_missing_values(data):
    # Create an instance of SimpleImputer
    imputer = SimpleImputer(strategy='mean')

    # Handle missing values by replacing them with the mean of each column
    data_imputed = imputer.fit_transform(data)

    print("Missing values handled. Imputed data:")
    print(data_imputed)

def perform_cross_validation(X, y, model='logistic', scoring='accuracy', cv=5):
    if model == 'logistic':
        clf = LogisticRegression()
    elif model == 'svm':
        clf = SVC()
    else:
        raise ValueError("Invalid model specified. Please choose 'logistic' or 'svm'.")

    scores = cross_val_score(clf, X, y, cv=cv, scoring=scoring)
    print(f"Cross Validation {scoring.capitalize()}:")
    print(scores)

def select_best_features(X, y, k=5):
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()]
    print("Selected Features:")
    print(selected_features)
def scale_data(X, scaler='standard'):
    if scaler == 'standard':
        scaler = StandardScaler()
    elif scaler == 'normal':
        scaler = MinMaxScaler()
    else:
        raise ValueError("Invalid scaler specified. Please choose 'standard' or 'normal'.")

    X_scaled = scaler.fit_transform(X)
    print("Scaled Data:")
    print(X_scaled)
def remove_low_variance_features(X, threshold=0.1):
    selector = VarianceThreshold(threshold=threshold)
    X_high_variance = selector.fit_transform(X)

    print("High variance features:")
    print(X_high_variance)

def split_data(X, y, test_size=0.2, random_state=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    print("Train/Test split:")
    print("X_train:", X_train)
    print("X_test:", X_test)
    print("y_train:", y_train)
    print("y_test:", y_test)

