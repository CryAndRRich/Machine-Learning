from typing import Tuple
import numpy as np
from ..base_model import ModelML

def sigmoid_function(x: np.ndarray) -> np.ndarray:
    """
    Computes the sigmoid function for input values

    Parameters:
    x: The input feature values 

    --------------------------------------------------
    Returns:
    np.ndarray: The sigmoid output for the input values
    """
    return 1 / (1 + np.exp(-x))

def log_loss(x: np.ndarray, 
             y: np.ndarray) -> np.ndarray:
    """
    Computes the logistic loss (binary cross-entropy) for a given prediction and true label

    Parameters:
    x: The true labels 
    y: The predicted probabilities 

    --------------------------------------------------
    Returns:
    np.ndarray: The binary cross-entropy loss for the prediction and label
    """
    return -(x * np.log(y)) - ((1 - x) * np.log(1 - y))

def cost_function(features: np.ndarray, 
                  labels: np.ndarray, 
                  weight: np.ndarray, 
                  bias: float) -> float:
    """
    Computes the logistic regression cost function using mean binary cross-entropy

    Parameters:
    features: The input features 
    labels: The target labels 
    weight: The current weight values 
    bias: The current bias value 

    --------------------------------------------------
    Returns:
    cost: The mean binary cross-entropy loss
    """
    m, n = features.shape
    prob = np.zeros(m)
    
    # Compute predicted probabilities
    for i in range(m):
        predict = 0
        for j in range(n):
            predict += features[i, j] * weight[j]
        prob[i] = sigmoid_function(predict + bias)
    
    # Calculate the cost using binary cross-entropy
    cost = np.mean(log_loss(labels, prob))
    return cost

def gradient_descent(features: np.ndarray, 
                     labels: np.ndarray, 
                     weight: np.ndarray, 
                     bias: float, 
                     learn_rate: float) -> Tuple[np.ndarray, float]:
    """
    Performs one step of gradient descent to update the model's weight and bias

    Parameters:
    features: The input features 
    labels: The target labels 
    weight: The current weight values 
    bias: The current bias value 
    learn_rate: The learning rate for gradient descent 

    --------------------------------------------------
    Returns:
    weight: The updated weight values after one step of gradient descent
    bias: The updated bias value after one step of gradient descent
    """
    m, n = features.shape

    weight_gradient = np.zeros(n)
    bias_gradient = 0
    
    # Compute gradients for weight and bias
    for i in range(m):
        predict = 0
        for j in range(n):
            predict += features[i, j] * weight[j]
        prob = sigmoid_function(predict + bias)

        for j in range(n):
            weight_gradient[j] += (prob - labels[i]) * features[i, j]
        bias_gradient += prob - labels[i]

    # Average the gradients
    weight_gradient /= m
    bias_gradient /= m

    # Update the weight and bias values based on the gradients and learning rate
    weight -= (learn_rate * weight_gradient)
    bias -= (learn_rate * bias_gradient)

    return weight, bias

class LogisticRegressionNumpy(ModelML):
    def __init__(self, 
                 learn_rate: float, 
                 number_of_epochs: int):
        """
        Initializes the Logistic Regression model using gradient descent

        Parameters:
        learn_rate: The learning rate for the gradient descent
        number_of_epochs: The number of training iterations to run
        """
        self.learn_rate = learn_rate
        self.number_of_epochs = number_of_epochs
    
    def fit(self, 
            features: np.ndarray, 
            labels: np.ndarray) -> None:
        """
        Trains the logistic regression model on the input data using gradient descent

        Parameters:
        features: The input features for training 
        labels: The target labels corresponding to the input features 
        """
        _, n = features.shape

        self.weight = np.zeros(n)  # Initialize weight to zeros
        self.bias = 0              # Initialize bias to 0

        # Perform gradient descent over the specified number of epochs
        for _ in range(self.number_of_epochs):
            cost = cost_function(features, labels, self.weight, self.bias)
            self.weight, self.bias = gradient_descent(features, labels, self.weight, self.bias, self.learn_rate)

    def predict(self, 
                test_features: np.ndarray, 
                test_labels: np.ndarray) -> None:
        """
        Predicts the labels for the test data using the trained Logistic Regression model

        Parameters:
        test_features: The input features for testing 
        test_labels: The target labels corresponding to the test features 
        """
        prob = sigmoid_function(np.dot(test_features, self.weight)) + self.bias
        predictions = (prob >= 0.5).astype(int)

        accuracy, f1 = self.evaluate(predictions, test_labels)
        print("Epoch: {}/{} Accuracy: {:.5f} F1-score: {:.5f}".format(
               self.number_of_epochs, self.number_of_epochs, accuracy, f1))
    
    def __str__(self) -> str:
        return "Logistic Regression (Numpy)"