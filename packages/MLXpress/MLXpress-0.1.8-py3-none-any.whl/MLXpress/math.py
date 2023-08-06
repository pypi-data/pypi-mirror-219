import numpy as np
import scipy.stats as stats

def pdf(x, distribution):
    """Calculate the probability density function (PDF) of a given distribution at a specific point and print the result."""
    pdf1 = distribution.pdf(x)
    print("Probability Density Function (PDF):", pdf1)

def hypothesis_test(data1, data2):
    """Perform a t-test to compare the means of two datasets and print the results."""
    t_statistic, p_value = stats.ttest_ind(data1, data2)
    print("T-Statistic:", t_statistic)
    print("P-Value:", p_value)

def distance_euclidean(x1, x2):
    """Calculate the Euclidean distance between two points and print the result."""
    distance = np.linalg.norm(x1 - x2)
    print("Euclidean Distance:", distance)

def linear_regression(x, y):
    """Perform linear regression and print the slope and intercept."""
    slope, intercept, _, _, _ = stats.linregress(x, y)
    print("Slope:", slope)
    print("Intercept:", intercept)

def covariance_matrix(matrix):
    """Calculate the covariance matrix of a given matrix and print the result."""
    covariance = np.cov(matrix, rowvar=False)
    print("Covariance Matrix:")
    print(covariance)


