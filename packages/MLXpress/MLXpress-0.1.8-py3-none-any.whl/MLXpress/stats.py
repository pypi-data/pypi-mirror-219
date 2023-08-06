import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import skew
def analyze(data):
    statistics = calculate_statistics(data)
    distribution_nature = determine_distribution_nature(data)
    print(f"The data is {distribution_nature} skewed")
    statistics['Distribution Nature'] = distribution_nature
    visualize_distribution(data)
    visualize_boxplot(data)
    visualize_histogram(data)

    return statistics

def calculate_statistics(data):
    mean = np.mean(data)
    median = np.median(data)
    mode = stats.mode(data).mode.item()
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    data_range = np.max(data) - np.min(data)
    variance = np.var(data)
    std_dev = np.std(data)

    stat = {
        'Mean': mean,
        'Median': median,
        'Mode': mode,
        'IQR': iqr,
        'Range': data_range,
        'Variance': variance,
        'Standard Deviation': std_dev
    }

    for stat_name, value in stat.items():
        print(f"{stat_name}: {value}")

    return stat

def visualize_distribution(data):
    sns.histplot(data, kde=True)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Distribution of Data')
    plt.show()

def visualize_boxplot(data):
    plt.boxplot(data)
    plt.xlabel('Data')
    plt.ylabel('Values')
    plt.title('Box Plot of Data')
    plt.show()

def visualize_histogram(data):
    plt.hist(data, bins='auto')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')
    plt.show()

def determine_distribution_nature(data):
    skewness = skew(data)

    if skewness > 0:
        return 'Right-skewed'
    elif skewness < 0:
        return 'Left-skewed'
    else:
        return 'Symmetric'
