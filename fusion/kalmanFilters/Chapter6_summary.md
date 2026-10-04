## Multivariate Kalman Filter
- We extend the Kalman filter developed in the univariate chapter to the full, generalized filter for linear problems. After reading this you will understand how a Kalman filter works and how to design and implement one for a (linear) problem of your choice.
- [Chapter 6 Notebook](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/06-Multivariate-Kalman-Filters.ipynb)


## Points to remember
- When starting to design kalman filters, start with differential equations that describe the dynamics of the system. First, try considering `discretized continous time kinematic model` (CV, CA, CT) and then move to more complex models. These equations can be integrated quite easily, and have a closed form solution, making the implementation of the filter easier.
- Pg:187 - Gaussians everywhere core concept of KF
- Pg:188 - **Designing KF means to decide (X, P, F, Q, Z, R, B, U)**
- Step1: Design State variables. Try to include correlation. But its a design choice. State variables can be observed variables (directly measured) or hidden variables (indirectly inferred from measurements). Assume x = [x_0, x_dot_0] to start with.
- Step2: Assign initial state covariance (P). Even if we know position and velocity are correlated, we don't know by how much. So, we can start with covariance of 0. A dog can move at max speed of 21m/s. If we assume initial state to be zero, we can be wrong 99.7% (3 sigma) by 21m/s. So, sigma = 21/3 = 7m/s. Variance = 49. So, P = [[0, 0], [0, 49]].
- Step3: Process model -> KF predicts state after discrete timestep. (called innovation, because we're predicting new information).Pg:193 eg: [500 0; 0 49]  becomes [512.35 24.5; 24.5 49] when running 5 iterations of predict() using CV model. Observe correlation introduction and no change in velocity.
- Step4: process noise: White noise (zero mean and variance Q=E[w * w.Transpose()].Here Discrete white noise considered). White noise has mean of zero, hence it doesn't affect mean, just the variance. Note that it depends on delta_t
- Step5: Designing control input (u). delta state = Bu. How control inputs influence change in state. Eg: if we have a car, and we know the acceleration, steering inputs, then we can use it to predict change in velocity and position. If we don't know the control input, then we can ignore it (u=0).
- Step6: Kf does the update step in measurement space. So, we need to convert the predicted state into measurements, for calculating the residual. We can't go from measurement to state, because state contains hidden variables. So, most often, measurements are not invertible. Residual is calculated in the measurement space. y = z - Hx, where H is the measurement function.
- Step7: Meas. noise difficult to find correlation b/w sensors, also not Gaussian always. generally, sensor measurements are not correlated. Hence, the measurement noise covariance matrix is diagonal. R = [[sigma_x^2, 0], [0, sigma_y^2]].
- Pg:199-201 Simple CV KF using filterpy objects
- Pg:202 Plot covariance of estimate. It's uncertainty we have, assuming we tell the truth
- Pg:203 saver class.
- Pg:206 Process Noise, concept of projecting P to F. Pg:207, how in cv model, vel doesn't change (height of ellipse no change, only tilting due to correlation). prior covariance (P) is projected to F (state transition matrix) to get new covariance (P') after prediction step. P' = F*P*F.T + Q. Q is process noise, which is added to account for uncertainty in model.
- Pg:209-210, System uncertainty (S=H*P*H.T + R) projecting to meas. space. Very similar to how P is projected to `F` in prediction step.
- Pg:210 `KG (0-1) range`, `KG~PHT`, scale/weight b/w to prediction & measurement. HT = converts from measurement Space to state space.
- Pg:215. Effect of including velocity in state vector allows to model changing velocity, else it will not react to state change

![effect_of_including_tracking_variables](images/effect_of_including_tracking_variables.PNG)

- If we're controlling a robot, we know the control input (u). But if we're tracking a moving object, we don't know the control input. So, we can include velocity in the state vector to model changing velocity. This allows the filter to react to changes in the object's motion.
- Pg:216 In localisation we know control I/P. **But for tracking include, V. So that I can model / try to predict changes in using correlation in model**. The correlation factor, is what allows us to calcualte velocity, even when we measure just the position. The correlation is propagated through process model (F), to Kalman gain, which is used to update state estimates (residual). This correction increases, as correlation increases.
- Pg:217 `KG going down is good sign of convergence, so is decreasing residual and variance (P_est)`. Good test would be provide offset in initial estimate, check if P converges

![P_est_verification](images/P_est_verification.png)

- Pg:218-226 - Effect of tuning different variables
- Q↑ -> less trust in prediction, closely follow measurements
- Less Q -> more trust in prediction, can lead to ignoring measurements.
- **>> R causes KF to ignore measurements. Can give smooth results, but not stable. Bad initial estimate can cause it to diverge** Check for P_est Value.

![effect_of_varying_q](images/effect_of_varying_q.PNG)

- Decent R values helps KF recover even in bad initial estimate

![effect_of_varying_r](images/effect_of_varying_r.PNG)

- Pg:221-222, effect of P (Higher P means more trust in measurements, Lesser P means ignores measurements,  P_est might not converge). **When Tracking dynamic objects, having >> P is justified as more uncertainty in movement**
- Pg:225-226, difference b/w high R and low R. if we lie to KF that R», then it will trust prediction more (can introduce More correlation). The correlation behaviour seen in filter output, needn't necessarily reflect the correlation in reality. The filter output depends on values of Q,R. Important to have same axis scale when viewing covariance values
- Filter initialization
    - Initialize the filter with first measurement, can use `H` to convert measurement to state space
    - Same way, R can be used to initialize `P`
    - Be careful when initializing hidden variables; need to ensure they make sense, and estimates got from them are reasonable
- Pg:228 = Batch Processing feature. Pg:229: **Residual must be centered around 0 and like noise**
- Pg:229 RTS smoother, Pg:30, Pros of using smoother
    - Take future values into consideration, when estimating current values. For example, if we're tracking a car, following a straight line, when it takes a left turn, the filter doesn't know, if its noise or actual physical change in direction. So, it will lag behind actual turn. If we have entire set of data (including future), we can use that to steer that preference to measurement, over prediction (straight line)
- Pg:232 - KF can be used to track higher Order derivatives. **Reality of tuning R, Q values is bit of art and science**
