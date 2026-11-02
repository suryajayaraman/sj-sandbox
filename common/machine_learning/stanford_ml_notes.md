# Stanford Machine Learning

## Introduction
- Supervised learning - both inputs and outputs are available
- Unsupervised learning - no explicit outputs available; trying to find clusters / patterns in input data
- Reinforcement learning
- Classification - finite set of outcomes
- Regression - output is continous variable

## Linear regression
- Linear regression- input variables are mapped to continous output function, output is linear combination of inputs
- Metric is based on cost function
- Gradient descent
    - Start with initial estimate of weights
    - Iterate until convergence
        - Find the cost of the initial estimate
        - Find the gradient w.r.t inputs
        - Update the weights, using combination of learning rate and gradient
        - If weighst are not changed by > 10e-3, declare as converged and break loop
- For linear models, analytical solution available, provided matrix `A` (in form Ax=B) has full rank. If it has lesser rank, many solutions are possible. If matrix doesn't have inverses, use `pseudoinverse`. pseudoinverse can be found using SVD (singular value decomposition). Possible reasons include
    - redundant features
    - too many features (m <= n)
- For linear models, there is only one global optima; no problem of getting stuck in local optima. For more complex  models, there can be many local minima. Depending on initialized values, we can arrive at different answers.
- Need to ensure input variables are of same scale (-1 to 1); else features will be weighted based on scale. similar to batch normalization.
- cost function = (1/2) * (h(x) - y)^2 => cost = -log(h(x)) when y=1. cost = 0, if y=1, and h(x) = 1. Basically, when the prediction is right, cost can be as low as zero. For incorrect predictions, cost can be as high as infinity.

## Logistic regression
- Discrete valued output - can be binary / multi-class classification. Usually, a threshold to determine output (0.5)
- Hypothesis is represented using sigmoid function. h(x) = 1 / (e^-z +1). Output is probability distribution over a class or multiple classes.
- Here, theta (estimated parameters) form a decision boundary between different classes
- e^-x is is non linear function and non-convex (no global minimum / maximum).
- cost function = -(1/m) * sum[y*log(h(x)) + (1-y)*log(1-h(x))]. When y=1, cost is only average of log(h(x)), when y = 0, cost = log(1-h(x))
- For multi-class classification, one vs all classification
- sigmoid gradient = g(z) * (1 - g(z)), where g(z) = sigmoid function

## Regularization
- problem of overfitting (fits training data too well, but fails to generalize to new examples)
- Options to fix overfitting
    - reduce number of features (manual selection or based on PCA)
    - Regulalization - reduces magnitude of theta_j, but keeps all features => many slightly useful features
- Why regularization reduces overfitting - Simpler hypothesis
- Just add -> alpha * sum(theta_j^2) to cost function
- Tradeoff between fitting the curve and smaller theta values

## Neural network algorithm
- Algorithms, that were inspired by biological neural networks, and presents highly non linear decision boundary

## Backpropagation
- Consider a 4 layer neural network, with some non linear activation function
- final output = a(4) = output of activation function of the 4th layer
- delta_4 = a(4) - y. delta_3 = (theta(3).T * delta_4) * g_dash((z(3)))
- NN algorithm
    - perform forward pass for each layer, till we get prediction
    - Compute error of prediction vs actual output
    - Compute gradient of output wrt parameters; do this recursively till first layer; then update parameters
- Initialize parameters randomly, to avoid symmetry problems

## Error analysis
- Start a simple algorithm, implement quickly
- Test on cross validation set
- plot learning curves to decide, if more data / features are required
- Try checking one sample in error of cross validation set, to see if there's a systematic trend in errors
- **Avoid premature optimization; evidence based decision making**
- Skewed data error metrics
    - confusion matrix, precision, recall
    - precision - of all the patients, whom we predicted have cancer, how many actually have cancer?
    - recall - of all the patients that actually have cancer, what fraction did we actually predcit as having cancer?
    - one parameter to modify for changing precision, recall - confidence threshold -> Higher precision, lower recall
        - For cases like cancer diagnosis, we'd want to ensure, no patient is missed. Hence, we'll most likely set lower confidence threshold -> Higher recall, lesser precision.
    - F1 score = PR / (P + R)

## Algorithms for different dataset sizes
- Choice of algorithms depends on training set size - number of samples, and also number of features available
- Using a large training set helps in preventing overfitting

## Support vector machines
- Alternative to logistic regression (trying to minimize the cost function)
