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
- Optimization objective for SVM is min(theta) -> y * cost(z) + (1-y) * cost(z) + 0.5*sum(theta^2), where z=prediction=theta*x
- cost(z) profile varies, when y=1 and y=0. When y=1, we want z (~output) to be much greater than 1, not just >=0. If y=0, we want z to be much lesser than -1.
- cost function for SVM becomes min(theta) cx + 0.5*sum(theta^2), subject to constraints, that theta*x>=1, when y=1 and theta*x<=-1, when y=0. Basically, SVM tries to increas the distance / decision boundary from each class. Hence, its called large margin classifier
- **TBD - understand math behind SVM**
    - cx part is negligible under certain considerations. Then, it becomes about minimizing 0.5*(theta^2)
    - theta^2 is just square of norm of theta -> magnitude of theta
    - Considering theta*x is just projection of X onto theta (assuming theta_0=0 for time being)
    - theta*x = projection needs to be >=1 (much larger than one) to satisfy the constraints. Hence, magnitude of theta has to be large, but its a minimisation problem
- c = (1/ lambda)
    - large C -> lambda=small -> lower bias, high variance (overfitting)
    - small C -> lambda=large -> higher bias, lower variance (underfitting)
- sigma^2 = large; very smooth transition; higher bias; lower variance
- sigma^2 = small; very sharp slope; lower bias; higher variance
- libSVM, liblinear implementations solve for theta;
- works well for problems, when m = small, n = large; if features are enough (prone to overfitting), best to use linear kernels
- Kernels available
    - Linear
    - Gaussian, need to choose sigma^2 (ensure feature scaling is done, before gaussian kernel)
    - polynomial kernels
    - others - need to ensure Mercer's theorem to ensure SVM packages don't diverge.
- **Not all similarity functions make valid kernels**


### Kernels
- Generic prediction formula => theta0 + theta1*f1 + theta2*f2 + theta3*f3 >= 0, where f1=x1, f2=x^2, f3=x^3
- For given input features x1,x2, compute new features, close to some landmarks (similarity functions). fx = similarlity(x,lx) = exp ( -|x-lx|^2 / 2sigma^2)
- Similarity functions, when x=lx, then fx=exp(-0) -> 2. When x is far from lx, fx=exp(-large number) -> 0
- Sigma in denominator is a hyperparameter to adjust the covariance thresholds
- Above similarity function is ~Gaussian distribution
- Possible options for landmarks - each of training example themselves. Basically, for each entry in training set X,Y, compute new features (f1, f2, ..) by comparing with other examples in training set, and append them as new features. Then, predict y=1, when theta*f >=0
- Training workflow - minimize theta, sum (y * cost(theta*f) + (1-y) * cost(theta *f) + |theta^2|)
- in above setup, the number of features is equal to number of training examples. When m=10k, theta = 10k order. Not tractable for larger datasets.
- SVMs are implemented with more tricks, than just kernels + logistic regression.
- Kernels are good choice for finding features for other algorithms, but they themselves with SVM don't work well.

## Multi class classification
- One vs all method. Train k SVMs, one to distinguish y=i from rest of classes. Pick class with highest probability of being true.

## Unsupervised learning
- unlabelled exmaples - find some structure in dataset
- Applications
    - Market segmentation (serve customers better, FB, Google)
    - Social network avanalysis
    - Organize computing clusters - understand datacenters better; organize resources bettern
    - Astronomical data analysis

### K-means algorithm

#### Input
- K (number of clusters)
- unlabelled dataset R^n dimension

#### Procedure
- Randomly initialize K cluster centroids
- Repeat
    - For each exmaple, find closest clusters for each training example. Distance can be L2 norm or similar
    - Update cluster centroid
    - If a cluster centroid has not data point with it, elminate it