import numpy as np


def l2_regularization(W, reg_strength):
    '''
    Computes L2 regularization loss on weights and its gradient

    Arguments:
      W, np array - weights
      reg_strength - float value

    Returns:
      loss, single value - l2 regularization loss
      gradient, np.array same shape as W - gradient of weight by l2 loss
    '''
    # TODO: Copy from previous assignment
    raise Exception("Not implemented!")

    return loss, grad


def softmax_with_cross_entropy(predictions, target_index):
    '''
    Computes softmax and cross-entropy loss for model predictions,
    including the gradient

    Arguments:
      predictions, np array, shape is either (N) or (batch_size, N) -
        classifier output
      target_index: np array of int, shape is (1) or (batch_size) -
        index of the true class for given sample(s)

    Returns:
      loss, single value - cross-entropy loss
      dprediction, np array same shape as predictions - gradient of predictions by loss value
    '''
    # TODO copy from the previous assignment
    raise Exception("Not implemented!")
    return loss, dprediction


class Param:
    '''
    Trainable parameter of the model
    Captures both parameter value and the gradient
    '''
    def __init__(self, value):
        self.value = value
        self.grad = np.zeros_like(value)

        
class ReLULayer:
    def __init__(self):
        pass

    def forward(self, X):
        # TODO copy from the previous assignment
        raise Exception("Not implemented!")

    def backward(self, d_out):
        # TODO copy from the previous assignment
        raise Exception("Not implemented!")
        return d_result

    def params(self):
        return {}


class FullyConnectedLayer:
    def __init__(self, n_input, n_output):
        self.W = Param(0.001 * np.random.randn(n_input, n_output))
        self.B = Param(0.001 * np.random.randn(1, n_output))
        self.X = None

    def forward(self, X):
        # TODO copy from the previous assignment
        raise Exception("Not implemented!")

    def backward(self, d_out):
        # TODO copy from the previous assignment
        
        raise Exception("Not implemented!")        
        return d_input

    def params(self):
        return { 'W': self.W, 'B': self.B }

    
class ConvolutionalLayer:
    def __init__(self, in_channels, out_channels,
                 filter_size, padding):
        '''
        Initializes the layer
        
        Arguments:
        in_channels, int - number of input channels
        out_channels, int - number of output channels
        filter_size, int - size of the conv filter
        padding, int - number of 'pixels' to pad on each side
        '''

        self.filter_size = filter_size
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.W = Param(
            np.random.randn(filter_size, filter_size,
                            in_channels, out_channels)
        )

        self.B = Param(np.zeros(out_channels))

        self.padding = padding


    def forward(self, X):
        padding = self.padding
        if padding > 0:
          X = np.insert(X, [0], [padding], axis=2)
          X = np.insert(X, X.shape[2], [padding], axis=2)
          X = np.insert(X, [0], [padding], axis=1)
          X = np.insert(X, X.shape[1], [padding], axis=1)
            
        batch_size, height, width, channels = X.shape

        out_height = 0
        out_width = 0
        
        result = np.zeros((batch_size, out_height, out_width, self.out_channels))
        
        # TODO: Implement forward pass
        # Hint: setup variables that hold the result
        # and one x/y location at a time in the loop below
        
        # It's ok to use loops for going over width and height
        # but try to avoid having any other loops
        W = self.W.value.reshape(-1, self.out_channels)
        for y in range(out_height):
            for x in range(out_width):
                Xk = X[:, y:y+self.filter_size, x:x+self.filter_size, :]
                Xk = Xk.reshape((batch_size, -1))
                result[:, y, x, :] = Xk.dot(W) + self.B.value
                
        # raise Exception("Not implemented!")
        
        return result


    def backward(self, d_out):
        # Hint: Forward pass was reduced to matrix multiply
        # You already know how to backprop through that
        # when you implemented FullyConnectedLayer
        # Just do it the same number of times and accumulate gradients
        
        X = self.X
        padding = self.padding

        batch_size, height, width, channels = X.shape
        _, out_height, out_width, out_channels = d_out.shape

        # TODO: Implement backward pass
        
        d_input = np.zeros_like(X)
        self.W.grad = np.zeros_like(self.W.value)
        self.B.grad = np.zeros_like(self.B.value)
        W = self.W.value.reshape((-1, out_channels))
        
        # Same as forward, setup variables of the right shape that
        # aggregate input gradient and fill them for every location
        # of the output

        # Try to avoid having any other loops here too
        filter_size = self.filter_size
        for y in range(out_height):
            for x in range(out_width):
                # TODO: Implement backward pass for specific location
                # Aggregate gradients for both the input and
                # the parameters (W and B)
                point = d_out[:, y, x, :]
                
                Xk = X[:, y:y+self.filter_size, x:x+self.filter_size, :]
                Xk = Xk.reshape((batch_size, -1))
                X_t = Xk.T

                d_W = X_t.dot(point)
                d_W = d_W.reshape((filter_size, filter_size, self.in_channels, out_channels))
                
                ones_t = np.ones((batch_size, )).T
                d_B = ones_t.dot(point)
                
                d_X_before_kernel = point.dot(W.T)
                d_X_before_kernel = d_X_before_kernel.reshape((batch_size, filter_size, filter_size, self.in_channels))
                
                self.W.grad += d_W
                self.B.grad += d_B
                d_input[:, y:y+filter_size, x:x+filter_size, :] += d_X_before_kernel

        # Delete padding if exists.
        d_input = d_input[:, padding:height-padding, padding:width-padding, :]
        return d_input

    def params(self):
        return { 'W': self.W, 'B': self.B }


class MaxPoolingLayer:
    def __init__(self, pool_size, stride):
        '''
        Initializes the max pool

        Arguments:
        pool_size, int - area to pool
        stride, int - step size between pooling windows
        '''
        self.pool_size = pool_size
        self.stride = stride
        self.X = None

    def forward(self, X):
       batch_size, height, width, channels = X.shape
        self.X = X
        
        # TODO: Implement maxpool forward pass
        # Hint: Similarly to Conv layer, loop on
        # output x/y dimension
        
        pool_size = self.pool_size
        stride = self.stride
        out_height = 1 + (height - pool_size) // stride
        out_width = 1 + (width - pool_size) // stride
        output = np.zeros((batch_size, out_height, out_width, channels))
        
        for y in range(out_height):
            for x in range(out_width):
                height_start = y * stride
                height_end = height_start + pool_size
                width_start = x * stride
                width_end = width_start + pool_size
                X_slice = X[:, height_start:height_end, 
                                      width_start:width_end, :]
                output[:, y, x, :] = np.max(X_slice, axis=(1, 2))
                
        return output
    
    def backward(self, d_out):
        pool_size = self.pool_size
        stride = self.stride
        X = self.X
        batch_size, height, width, in_channels = X.shape
        _, out_height, out_width, out_channels = d_out.shape
        
        d_input = np.zeros_like(X)
        
        for batch in range(batch_size):
            for y in range(out_height):
                for x in range(out_width):
                    for channel in range(in_channels):
                        mask = np.zeros((pool_size, pool_size))
                        y_source = y * stride
                        x_source = x * stride
                        pool = X[batch,
                                 y_source:np.minimum(y_source+pool_size, height),
                                 x_source:np.minimum(x_source+pool_size, width), channel]
                        
                        maximum = np.max(pool)
                        max_count = np.count_nonzero(pool == maximum)
                        argmax = np.argwhere(pool==maximum)
                        mask[argmax[:,0], argmax[:,1]] = d_out[batch, y, x, channel] / max_count
                        
                        d_input[batch, y_source:y_source+pool_size, x_source:x_source+pool_size, channel] += mask
                        
        return d_input
    
    def params(self):
        return {}


class Flattener:
    def __init__(self):
        self.X_shape = None

    def forward(self, X):
        self.X_shape = X.shape
        batch_size, height, width, channels = X.shape

        # TODO: Implement forward pass
        # Layer should return array with dimensions
        # [batch_size, hight*width*channels]
        return X.reshape((batch_size, -1))
    
    def backward(self, d_out):
        batch_size, height, width, channels = self.X_shape
        
        return d_out.reshape((batch_size, height, width, channels))

    def params(self):
        # No params!
        return {}
