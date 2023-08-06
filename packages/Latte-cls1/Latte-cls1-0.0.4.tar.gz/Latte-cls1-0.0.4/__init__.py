import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import svm,tree

def linear(filename, cl1, cl2, predict_value):
    # Read the data from the CSV file
    x = []
    y = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x.append(float(row[cl1]))
            y.append(float(row[cl2]))

    # Convert input arrays to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Calculate the number of data points
    n = len(x)

    # Calculate the mean of x and y
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # Calculate the slope and intercept of the regression line
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    slope = numerator / denominator
    
    slp=f"slope : {slope}"
    
    intercept = y_mean - slope * x_mean
    intc=f"intercept: {intercept}"
    # Plot the data points and regression line
    plt.scatter(x, y, color='blue', label='Data')
    plt.plot(x, slope * x + intercept, color='red', label='Regression Line')

    # Predict the value for the given input
    prediction = slope * predict_value + intercept
    
    pred=f"prediction : {prediction}"
    
    plt.scatter(predict_value, prediction, color='green', label='Prediction')
    plt.annotate(f'({predict_value}, {prediction:.2f})',
                 (predict_value, prediction), xytext=(20, -20),
                 textcoords='offset points', color='green')

    # Set the labels and title of the plot
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Regression')

    # Display the legend and show the plot
    plt.legend()
    plt.show()

    # Return the slope, intercept, and prediction as results
    return slp, intc, pred


def logistic(filename, cl1, cl2, predict_value):
    # Read the data from the CSV file
    x = []
    y = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x.append([float(row[cl1])])
            y.append(float(row[cl2]))

    # Convert input arrays to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Perform logistic regression
    model = LogisticRegression()
    model.fit(x, y)

    # Plot the data points
    plt.scatter(x, y, color='blue', label='Data')

    # Plot the logistic regression curve
    x_range = np.linspace(min(x), max(x), 1000).reshape(-1, 1)
    y_range = model.predict_proba(x_range)[:, 1]
    plt.plot(x_range, y_range, color='red', label='Logistic Regression')

    # Predict the probability for the given input
    predict_proba = model.predict_proba([[predict_value]])[0, 1]
    predict = model.predict([[predict_value]])[0]
    plt.scatter(predict_value, predict_proba, color='green', label='Prediction')
    plt.annotate(f'({predict_value}, {predict_proba:.2f})',
                 (predict_value, predict_proba), xytext=(20, -20),
                 textcoords='offset points', color='green')

    # Set the labels and title of the plot
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Logistic Regression')

    # Display the legend and show the plot
    plt.legend()
    plt.show()

    # Return the probability and prediction as results
    return f"probability : {predict_proba}", f"prediction : {predict}"





def dtree(filename, cl1, cl2, predict_value):
    # Read the data from the CSV file
    x = []
    y = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x.append([float(row[cl1])])
            y.append(float(row[cl2]))

    # Convert input arrays to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Perform decision tree classification
    model = tree.DecisionTreeClassifier()
    model.fit(x, y)

    # Plot the data points
    plt.scatter(x, y, color='blue', label='Data')

    # Plot the decision tree boundary
    x_range = np.linspace(min(x), max(x), 1000).reshape(-1, 1)
    y_range = model.predict(x_range)
    plt.plot(x_range, y_range, color='red', label='Decision Tree')

    # Predict the class for the given input
    predict = model.predict([[predict_value]])[0]
    plt.scatter(predict_value, predict, color='green', label='Prediction')
    plt.annotate(f'({predict_value}, {predict})',
                 (predict_value, predict), xytext=(20, -20),
                 textcoords='offset points', color='green')

    # Set the labels and title of the plot
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Decision Tree')

    # Display the legend and show the plot
    plt.legend()
    plt.show()

    # Return the prediction as a result
    return f"prediction: {predict}"


def matrix_ml(matrix1, matrix2):
    # Perform matrix multiplication
    result = np.dot(matrix1, matrix2)
    return result

def matrix_add(matrix1, matrix2):
    # Perform matrix addition
    result = np.add(matrix1, matrix2)
    return result