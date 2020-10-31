import numpy as np
import matplotlib.pyplot as plt



class MLP:
    " Multi-layer perceptron "
    def __init__(self, sizes, beta=1, momentum=0.9):

        """
        sizes is a list of length four. The first element is the number of features 
                in each samples. In the MNIST dataset, this is 784 (28*28). The second 
                and the third  elements are the number of neurons in the first 
                and the second hidden layers, respectively. The fourth element is the 
                number of neurons in the output layer which is determined by the number 
                of classes. For example, if the sizes list is [784, 5, 7, 10], this means 
                the first hidden layer has 5 neurons and the second layer has 7 neurons. 
        
        beta is a scalar used in the sigmoid function
        momentum is a scalar used for the gradient descent with momentum 
        """
        self.beta = beta
        self.momentum = momentum

        self.nin = sizes[0] # number of features in each sample
        self.nhidden1 = sizes[1] # number of neurons in the first hidden layer
        self.nhidden2 = sizes[2] # number of neurons in the second hidden layer
        self.nout = sizes[3] # number of classes / the number of neurons in the output layer


        # Initialise the network of two hidden layers
        self.weights1 = (np.random.rand(self.nin+1,self.nhidden1)-0.5)*2/np.sqrt(self.nin) # hidden layer 1
        self.weights2 = (np.random.rand(self.nhidden1+1,self.nhidden2)-0.5)*2/np.sqrt(self.nhidden1) # hidden layer 2
        self.weights3 = (np.random.rand(self.nhidden2+1,self.nout)-0.5)*2/np.sqrt(self.nhidden2) # output layer


    def train(self, inputs, targets, eta, niterations):
        """
        inputs is a numpy array of shape (num_train, D) containing the training images
                    consisting of num_train samples each of dimension D.

        targets is a numpy array of shape (num_train, D) containing the training labels
                    consisting of num_train samples each of dimension D.

        eta is the learning rate for optimization 
        niterations is the number of iterations for updating the weights 

        """
        ndata = np.shape(inputs)[0] # number of data samples
        # adding the bias
        inputs = np.concatenate((inputs, -np.ones((ndata, 1))), axis=1)

        # numpy array to store the update weights
        updatew1 = np.zeros((np.shape(self.weights1)))
        updatew2 = np.zeros((np.shape(self.weights2)))
        updatew3 = np.zeros((np.shape(self.weights3)))

        self.Errors = []
        for n in range(niterations):

            #############################################################################
            # TODO: implement the training phase of one iteration which consists of two phases:
            # the forward phase and the backward phase. you will implement the forward phase in 
            # the self.forwardPass method and return the outputs to self.outputs. Then compute 
            # the error (hints: similar to what we did in the lab). Next is to implement the 
            # backward phase where you will compute the derivative of the layers and update 
            # their weights. 
            #############################################################################

            # forward phase 
            self.outputs = self.forwardPass(inputs)

            # Error using the sum-of-squares error function
            error = 0.5 * np.sum((self.outputs - targets) ** 2)

            if np.mod(n, 100) == 0:
                self.Errors.append(error)
                print("Iteration: ", n, " Error: ", error)

            # backward phase 
            # Compute the derivative of the output layer. NOTE: you will need to compute the derivative of 
            # the softmax function. Hints: equation 4.55 in the book. 
            # deltao = (self.outputs - targets) * (self.outputs - self.outputs ** 2)
            deltao = (self.outputs - targets) * self.outputs * (1 - self.outputs)

            # compute the derivative of the second hidden layer

            deltah2 = self.beta * self.hidden2 * (1.0 - self.hidden2) * (np.dot(deltao, np.transpose(self.weights3)))


            # compute the derivative of the first hidden layer
            deltah1 = self.beta * self.hidden1 * (1.0 - self.hidden1) * (np.dot(deltah2[:, :-1], np.transpose(self.weights2)))

            # update the weights of the three layers: self.weights1, self.weights2 and self.weights3
            # here you can update the weights as we did in the week 4 lab (using gradient descent) 
            # but you can also add the momentum

            updatew1 = eta * np.dot(np.transpose(inputs), deltah1[:, :-1])  + self.momentum * updatew1
            updatew2 = eta * np.dot(np.transpose(self.hidden1), deltah2[:, :-1])  + self.momentum * updatew2
            updatew3 = eta * np.dot(np.transpose(self.hidden2), deltao)   + self.momentum * updatew3

            self.weights1 -= updatew1
            self.weights2 -= updatew2
            self.weights3 -= updatew3

            #############################################################################
            # END of YOUR CODE 
            #############################################################################




    def forwardPass(self, inputs):
        """
            inputs is a numpy array of shape (num_train, D) containing the training images
                    consisting of num_train samples each of dimension D.  
        """
        #############################################################################
        # TODO: Implement the forward phase of the model. It has two hidden layers 
        # and the output layer. The activation function of the two hidden layers is 
        # sigmoid function. The output layer activation function is the softmax function
        # because we are working with multi-class classification. 
        #############################################################################

        # layer 1 
        # compute the forward pass on the first hidden layer with the sigmoid function

        self.hidden1 = np.dot(inputs, self.weights1)    #(9000, 785) (785, 5)
        self.hidden1 = self.sigmoid_fun(self.hidden1)   #(9000, 5)
        self.hidden1 = np.concatenate((self.hidden1, -np.ones((np.shape(inputs)[0], 1))), axis=1) # (9000,6)


        # layer 2
        # compute the forward pass on the second hidden layer with the sigmoid function
        self.hidden2 = np.dot(self.hidden1, self.weights2)               # (9000,6) (6, 5)
        self.hidden2 = self.sigmoid_fun(self.hidden2)                   # (9000,5)
        self.hidden2 = np.concatenate((self.hidden2, -np.ones((np.shape(self.hidden1)[0], 1))), axis=1)  # (9000,6)

        # output layer
        # compute the forward pass on the output layer with softmax function
        outputs = np.dot(self.hidden2, self.weights3)  # (9000,6) (6, 10)
        outputs = self.softmax_fun(outputs)            # (9000,10)
        # print(outputs)
        #############################################################################
        # END of YOUR CODE 
        #############################################################################
        return outputs


    def evaluate(self, X, y):
        """ 
            this method is to evaluate our model on unseen samples 
            it computes the confusion matrix and the accuracy 
    
            X is a numpy array of shape (num_train, D) containing the testing images
                    consisting of num_train samples each of dimension D. 
            y is  a numpy array of shape (num_train, D) containing the testing labels
                    consisting of num_train samples each of dimension D.
        """

        inputs = np.concatenate((X,-np.ones((np.shape(X)[0],1))),axis=1)
        outputs = self.forwardPass(inputs)
        nclasses = np.shape(y)[1]

        # 1-of-N encoding
        outputs = np.argmax(outputs,1)
        targets = np.argmax(y,1)

        cm = np.zeros((nclasses,nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

        print("The confusion matrix is:")
        print(cm)
        self.accuracy = np.trace(cm)/np.sum(cm)*100
        print("The accuracy is ",np.trace(cm)/np.sum(cm)*100)


    def sigmoid_fun(self, x):
        x = self.beta * x
        return 1/(1 + np.exp(-x))


    def softmax_fun(self, x):
        len  = np.shape(x)[0]
        for i in range(len):
            v = x[i]
            for j in range(np.shape(v)[0]):
                x[i][j] = np.exp(v[j]) / np.sum(np.exp(v))

        return x

    def plot_error(self, niter):
        X = [x for x in range(0, int(niter), 100)]
        Y = self.Errors
        plt.plot(X, Y, 'g*-')


import pickle, gzip

f = gzip.open('mnist.pkl.gz','rb')
tset, vset, teset = pickle.load(f, encoding='latin1')
print(tset[0].shape, vset[0].shape, teset[0].shape)
f.close()

# Just use the first 9000 images for training
tread = 9000
train_in = tset[0][:tread, :]

# This is a little bit of work -- 1 of N encoding
# Make sure you understand how it does it
train_tgt = np.zeros((tread,10))
for i in range(tread):
    train_tgt[i,tset[1][i]] = 1

# and use 1000 images for testing
teread = 1000
test_in = teset[0][:teread,:]
test_tgt = np.zeros((teread,10))
for i in range(teread):
    test_tgt[i,teset[1][i]] = 1


# sizes = [784,5,5,10] # 784 is the number of pixels of the images and 10 is the number of classes
# classifier = MLP(sizes)
# classifier.train(train_in, train_tgt, 0.1, 1000)
# classifier.evaluate(test_in, test_tgt)

best_sizes = [784, 50, 20, 10]
best_beta = 0.9
best_momentum = 0
best_lr = 0.001 # best learning rate
best_niterations = 2500
best_classifier = MLP(sizes = best_sizes, beta=best_beta, momentum=best_momentum)
best_classifier.train(train_in, train_tgt, best_lr, best_niterations)
best_classifier.evaluate(test_in, test_tgt)

best_classifier.plot_error(best_niterations)
plt.xlabel('the number of iterations')
plt.ylabel('the errors')
accuracy = round(best_classifier.accuracy, 2)
plt.text(best_niterations/2, 4000, r'$accuracy:\ '+str(accuracy)+'\%$', fontdict={'size':'12', 'color':'r'})
plt.title('sizes:{}, beta:{}, momentum:{}, lr:{}, '
          'niter:{}'.format(best_sizes, best_beta, best_momentum, best_lr, best_niterations))
plt.show()