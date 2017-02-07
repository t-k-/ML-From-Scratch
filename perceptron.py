from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import numpy as np
import math

def sigmoid(x):
	return 1/(1+np.exp(-x))

def sigmoid_gradient(x):
	return sigmoid(x)*(1-sigmoid(x))

def categorical_to_binary(x):
	n_col = np.amax(x)+1
	binarized = np.zeros((len(x), n_col))
	for i in range(len(x)):
		binarized[i, x[i]] = 1
	return binarized	

data = datasets.load_iris()
X = data.data
y = data.target
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

y_train = categorical_to_binary(y_train)
y_test = categorical_to_binary(y_test)

x_train = normalize(x_train)
x_test = normalize(x_test)

# Configuration
n_neurons = len(y_train[0,:])
n_iterations = 80000
n_samples = len(x_train)
n_features = len(x_train[0])
learning_rate = 0.001

# Initial weights between [-1/sqrt(N), 1/sqrt(N)] (w - hidden, v - output)
a = -1/math.sqrt(n_features)
b = -a
w = (b-a)*np.random.random((len(x_train[0]), n_neurons)) + a

errors = []
for i in range(n_iterations):
	# Calculate outputs
	neuron_input = np.dot(x_train,w)
	neuron_output = sigmoid(neuron_input)
	
	mean_squared_error = np.mean(np.power(y_train - neuron_output, 2))
	errors.append(mean_squared_error)
	
	# Calculate the loss gradient
	w_gradient = -2*(y_train - neuron_output)*sigmoid_gradient(neuron_input)

	# Update weights
	w -= learning_rate*x_train.T.dot(w_gradient)


# Plot the training error
plt.plot(range(n_iterations), errors)
plt.ylabel('Training Error')
plt.xlabel('Iterations')
plt.show()

# Predict x_test
# Calculate outputs
y_pred = np.round(sigmoid(np.dot(x_test,w)))

# Print prediction and true output
print y_pred
print y_test
print "Accuracy:", accuracy_score(y_test, y_pred)

