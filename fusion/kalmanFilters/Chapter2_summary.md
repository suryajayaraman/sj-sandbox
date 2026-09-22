## The Discrete Bayes Filter
- Introduces the discrete Bayes filter. From this you will learn the probabilistic (Bayesian) reasoning that underpins the Kalman filter in an easy to digest form.
- [Chapter 2 Notebook](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/9e3d2f6ed023d937587cf2ef2ecfbf7afc3d8054//02-Discrete-Bayes.ipynb)


## Points to remember
- Pg:57, Resources -books - Sebastian Thrun,
- Pg 58: **Frequentist vs Bayesian. Prior state information Inclusion means Bayesian.**
- Pg:57-58 setting up of log Tracking problem, hallway setup By:55, 1st measurements door (prior uniform distribution, after 1 meas, 33% on 3 locations)
- Pg:60, Noisy sensors / not perfect sensors. * Scaling to produce exact prob. distribution)
- Pg:62, last paragraph - **Likelihood, [How each position is likely to receive measurement]**
- Pg:64 Incorporating Perfect Movement → Pg:67-68 @ having imperfect sensors, sensor data distribution how prediction reduces our belief.
- Pg:67 convolve operation introduction for generalisation
- Pg:71 convolution in stochastic vs deterministic
- Pg:75, Discrete bayes filter pseudocode.
- Pg:79, bad sensor data recovery.
- Pg:79 Drawbacks of diccrete Bayes filter scaling (x O(n^n) where n = state dimension, curese of dimensionality -> not desirable in all cases, 4th = requires change in input state
- Pg:80 - we control commands for prediction
- Pg 84 - Bayes theorem and Total prob introduction
