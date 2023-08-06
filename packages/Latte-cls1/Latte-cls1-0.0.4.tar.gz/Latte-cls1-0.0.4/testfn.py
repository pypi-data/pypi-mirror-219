import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def logistic_regression(data, predict_value):
    # Extract the features and labels from the data
    x = data[:, :-1]
    y = data[:, -1]

    # Perform logistic regression
    model = LogisticRegression()
    model.fit(x, y)

    # Plot the data points
    plt.scatter(x[:, 0], x[:, 1], c=y, cmap='bwr', label='Data')

    # Plot the logistic regression curve
    x_range = np.linspace(min(x[:, 0]), max(x[:, 0]), 100)
    y_range = np.linspace(min(x[:, 1]), max(x[:, 1]), 100)
    xx, yy = np.meshgrid(x_range, y_range)
    xy = np.column_stack([xx.ravel(), yy.ravel()])
    z = model.predict_proba(xy)[:, 1].reshape(xx.shape)
    plt.contour(xx, yy, z, levels=[0.5], colors='red', linestyles='dashed',
                label='Logistic Regression')

    # Predict the probability for the given input
    predict_proba = model.predict_proba([predict_value])[0, 1]
    predict = model.predict([predict_value])[0]
    plt.scatter(predict_value[0], predict_value[1], color='green', label='Prediction')
    plt.annotate(f'({predict_value[0]}, {predict_value[1]})\nProb: {predict_proba:.2f}',
                 (predict_value[0], predict_value[1]), xytext=(20, -20),
                 textcoords='offset points', color='green')

    # Set the labels and title of the plot
    plt.xlabel('Age')
    plt.ylabel('Weight')
    plt.title('Logistic Regression')

    # Display the legend and show the plot
    plt.legend()
    plt.show()

    # Return the probability and prediction as results
    return f"probability : {predict_proba}", f"prediction : {predict}"


# Load the dataset
data = np.array([
    [60, 58, 1],
    [61, 90, 1],
    [74, 96, 1],
    [57, 72, 1],
    [63, 62, 1],
    [68, 79, 1],
    [66, 69, 1],
    [77, 96, 1],
    [63, 96, 1],
    [54, 54, 0],
    [63, 57, 0],
    [76, 99, 0],
    [60, 74, 0],
    [61, 73, 0],
    [65, 85, 0],
    [79, 80, 0]
])

# Specify the predict value
predict_value = [70, 75]

# Perform logistic regression and plot the results
probability, prediction = logistic_regression(data, predict_value)
print(probability)
print(prediction)
