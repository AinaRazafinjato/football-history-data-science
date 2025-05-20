def plot_data(data):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(data, kde=True)
    plt.title('Data Distribution')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.show()

def summary_statistics(data):
    return {
        'mean': data.mean(),
        'median': data.median(),
        'std_dev': data.std(),
        'min': data.min(),
        'max': data.max(),
        'count': data.count()
    }

def correlation_analysis(data):
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()