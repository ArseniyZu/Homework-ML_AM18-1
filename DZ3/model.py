import numpy as np

from layers import FullyConnectedLayer, ReLULayer, softmax_with_cross_entropy, l2_regularization, softmax


class TwoLayerNet:
    """ Neural network with two fully connected layers """

    def __init__(self, n_input, n_output, hidden_layer_size, reg):
        """
        Initializes the neural network

        Arguments:
        n_input, int - dimension of the model input
        n_output, int - number of classes to predict
        hidden_layer_size, int - number of neurons in the hidden layer
        reg, float - L2 regularization strength
        """
        self.reg = reg
        # TODO Create necessary layers
        # raise Exception("Not implemented!")
        self.layer1 = FullyConnectedLayer(n_input, hidden_layer_size)
        self.layer2 = ReLULayer()
        self.layer3 = FullyConnectedLayer(hidden_layer_size, n_output)


    def compute_loss_and_gradients(self, X, y):
        """
        Computes total loss and updates parameter gradients
        on a batch of training examples

        Arguments:
        X, np array (batch_size, input_features) - input data
        y, np array of int (batch_size) - classes
        """
        # Before running forward and backward pass through the model,
        # clear parameter gradients aggregated from the previous pass
        # TODO Set parameter gradient to zeros
        # Hint: using self.params() might be useful!
        # raise Exception("Not implemented!")
        par = self.params()
        for i in par:
          params = par[i]
          params.grad = np.zeros_like(params.grad) 

        # TODO Compute loss and fill param gradients
        # by running forward and backward passes through the model
        forward1, cache1 = self.layer1.forward(X)
        forward2, cache2 = self.layer2.forward(forward1)
        forward3, cache3 = self.layer3.forward(forward2)
        loss, grad_of_pred = softmax_with_cross_entropy(forward3, y)

        backward1 = self.layer3.backward(grad_of_pred, cache3)
        backward2 = self.layer2.backward(backward1, cache2)
        backward3 = self.layer1.backward(backward2, cache1)

        # After that, implement l2 regularization on all params
        # Hint: self.params() is useful again!
        # raise Exception("Not implemented!")

        for i in par:
          params = par[i]
          loss += l2_regularization(par[i].value, self.reg)[0]
          params.grad += l2_regularization(par[i].value, self.reg)[1]

        return loss

    def predict(self, X):
        """
        Produces classifier predictions on the set

        Arguments:
          X, np array (test_samples, num_features)

        Returns:
          y_pred, np.array of int (test_samples)
        """
        # TODO: Implement predict
        # Hint: some of the code of the compute_loss_and_gradients
        # can be reused
        pred = np.zeros(X.shape[0], np.int)
        forward1, cache1 = self.layer1.forward(X)
        forward2, cache2 = self.layer2.forward(forward1)
        forward3, cache3 = self.layer3.forward(forward2)
        probability = softmax(forward3)
        pred = np.argmax(probability, axis = 1)

        # raise Exception("Not implemented!")
        return pred

    def params(self):
        result = {"W1": self.layer1.W, "B1": self.layer1.B, 
                  "W2": self.layer3.W, "B2": self.layer3.B}

        # TODO Implement aggregating all of the params

        # raise Exception("Not implemented!")

        return result
