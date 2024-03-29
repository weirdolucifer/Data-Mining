import csv
import random
import math
random.seed(137777)

with open('Datasets/iris/iris.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader, None) 
    dataset = list(csvreader)


for row in dataset:
    row[4] = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"].index(row[4])
    row[:4] = [float(row[j]) for j in xrange(len(row))]
    


random.shuffle(dataset)
datatrain = dataset[:int(len(dataset) * 0.85)]
datatest = dataset[int(len(dataset) * 0.85):]
train_X = [data[:4] for data in datatrain]
train_y = [data[4] for data in datatrain]
test_X = [data[:4] for data in datatest]
test_y = [data[4] for data in datatest]

def matrix_mul_bias(A, B, bias): # Matrix multiplication (for Testing)
    C = [[0 for i in xrange(len(B[0]))] for i in xrange(len(A))]    
    for i in xrange(len(A)):
        for j in xrange(len(B[0])):
            for k in xrange(len(B)):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] += bias[j]
    return C

def vec_mat_bias(A, B, bias): # Vector (A) x matrix (B) multiplication
    C = [0 for i in xrange(len(B[0]))]
    for j in xrange(len(B[0])):
        for k in xrange(len(B)):
            C[j] += A[k] * B[k][j]
            C[j] += bias[j]
    return C


def mat_vec(A, B): # Matrix (A) x vector (B) multipilicatoin (for backprop)
    C = [0 for i in xrange(len(A))]
    for i in xrange(len(A)):
        for j in xrange(len(B)):
            C[i] += A[i][j] * B[j]
    return C

def sigmoid(A, deriv=False): 
    if deriv: # derivation of sigmoid (for backprop)
        for i in xrange(len(A)):
            A[i] = A[i] * (1 - A[i])
    else:
        for i in xrange(len(A)):
            A[i] = 1 / (1 + math.exp(-A[i]))
    return A


alfa = 0.005
epoch = 600
neuron = [4, 3] 

# Initiate weight and bias with 0 value
weight = [[0 for j in xrange(neuron[1])] for i in xrange(neuron[0])]
bias = [0 for i in xrange(neuron[1])]

# Initiate weight with random between -1.0 ... 1.0
for i in xrange(neuron[0]):
    for j in xrange(neuron[1]):
        weight[i][j] = 2 * random.random() - 1

for e in xrange(epoch):
    cost_total = 0
    for idx, x in enumerate(train_X): # Update for each data
        
        # Forward propagation
        h_1 = vec_mat_bias(x, weight, bias)
        X_1 = sigmoid(h_1)
        
        # Convert to One-hot target
        target = [0, 0, 0]
        target[int(train_y[idx])] = 1

        # Cost function, Square Root Eror
        eror = 0
        for i in xrange(3):
            eror +=  0.5 * (target[i] - X_1[i]) ** 2 
        cost_total += eror

        # Backward propagation
        # Update weight_2 and bias_2 (layer 2)
        delta = []
        for j in xrange(neuron[1]):
            delta.append(-1 * (target[j]-X_1[j]) * X_1[j] * (1-X_1[j]))

        for i in xrange(neuron[0]):
            for j in xrange(neuron[1]):
                weight[i][j] -= alfa * (delta[j] * x[i])
                bias[j] -= alfa * delta[j]

    cost_total /= len(train_X)
    if(e % 100 == 0):
        print cost_total



res = matrix_mul_bias(test_X, weight, bias)


preds = []
for r in res:
    preds.append(max(enumerate(r), key=lambda x:x[1])[0])

print preds

acc = 0.0
for i in xrange(len(preds)):
    if preds[i] == int(test_y[i]):
        acc += 1
print acc / len(preds) * 100, "%"
