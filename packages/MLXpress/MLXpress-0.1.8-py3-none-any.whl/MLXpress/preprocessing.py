from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pandas as pd
def handle_missing_values(data):
    """
      Handle missing values in the input data by replacing them with the mean of each column.

      Parameters:
          data (numpy.ndarray or pandas.DataFrame): Input data with missing values.

      Returns:
          None
      """
    # Create an instance of SimpleImputer
    imputer = SimpleImputer(strategy='mean')

    # Handle missing values by replacing them with the mean of each column
    data_imputed = imputer.fit_transform(data)

    print("Missing values handled. Imputed data:")
    print(pd.DataFrame(data_imputed, columns=data.columns))

def perform_cross_validation(X, y, model='logistic', scoring='accuracy', cv=2):
    """
        Perform cross-validation on the input data using the specified model.

        Parameters:
            X (numpy.ndarray or pandas.DataFrame): Input features.
            y (numpy.ndarray or pandas.Series): Target variable.
            model (str, optional): Model to use for cross-validation. Default is 'logistic'.
            scoring (str, optional): Scoring metric for cross-validation. Default is 'accuracy'.
            cv (int, optional): Number of cross-validation folds. Default is 5.

        Returns:
            None
        """
    if model == 'logistic':
        clf = LogisticRegression(max_iter=10000)
    elif model == 'svm':
        clf = SVC()
    else:
        raise ValueError("Invalid model specified. Please choose 'logistic' or 'svm'.")

    scores = cross_val_score(clf, X, y, cv=cv, scoring=scoring)
    print(f"Cross Validation {scoring.capitalize()}:")
    for i, score in enumerate(scores):
        print(f"Fold {i + 1}: {score:.4f}")  # Print cross-validation scores with 4 decimal places

def select_best_features(X, y, k='all'):
    """
       Select the top k best features using the specified scoring function.

       Parameters:
           X (numpy.ndarray or pandas.DataFrame): Input features.
           y (numpy.ndarray or pandas.Series): Target variable.
           k (int, optional): Number of top features to select. Default is 5.

       Returns:
           None
       """
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()]
    print("Selected Features:")
    print(selected_features.tolist())
def scale_data(X, scaler='standard'):
    """
        Scale the input data using the specified scaler.

        Parameters:
            X (numpy.ndarray or pandas.DataFrame): Input data to be scaled.
            scaler (str, optional): Scaler to use for scaling. Default is 'standard'.

        Returns:
            None
        """
    if scaler == 'standard':
        scaler = StandardScaler()
    elif scaler == 'normal':
        scaler = MinMaxScaler()
    else:
        raise ValueError("Invalid scaler specified. Please choose 'standard' or 'normal'.")

    X_scaled = scaler.fit_transform(X)
    print("Scaled Data:")
    print(pd.DataFrame(X_scaled, columns=X.columns))
def remove_low_variance_features(X, threshold=0.1):
    """
       Remove features with low variance from the input data.

       Parameters:
           X (numpy.ndarray or pandas.DataFrame): Input data.
           threshold (float, optional): Threshold for variance. Features with variance below this threshold will be removed. Default is 0.1.

       Returns:
           None
       """
    selector = VarianceThreshold(threshold=threshold)
    X_high_variance = selector.fit_transform(X)
    print("High variance features:")
    print(pd.DataFrame(X_high_variance, columns=X.columns))



def split_data(X, y, test_size=0.2, random_state=None):
    """
        Split the input data into training and testing sets.

        Parameters:
            X (numpy.ndarray or pandas.DataFrame): Input features.
            y (numpy.ndarray or pandas.Series): Target variable.
            test_size (float, optional): Proportion of the data to be used for testing. Default is 0.2.
            random_state (int or None, optional): Random seed for reproducibility. Default is None.

        Returns:
            None
        """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    print("Train/Test split:")
    print("X_train:\n", X_train)
    print("X_test:\n", X_test)
    print("y_train:\n", y_train)
    print("y_test:\n", y_test)



