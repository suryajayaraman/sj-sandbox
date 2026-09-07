# Common concepts in ML and DL

## Loss functions
- Cross Entropy ???
- label smoothing CE ???
- Bitempered logistic loss function ???
- Focal loss function ???
- Taylor loss function ???

## Miscellaneous
- [snapshot learning and cyclic lr](https://www.kaggle.com/c/tgs-salt-identification-challenge/discussion/65347)
- [MoA 1st place solution](https://www.kaggle.com/c/lish-moa/discussion/201510#1102840)
- [forward selection ensemble method](https://www.kaggle.com/cdeotte/forward-selection-oof-ensemble-0-942-private)


## ML
### linear regression scikit-learn package
- sklearn.linear_model.LinearRegressn() class is supervised
reression tdhnique an it can be used ot fit lines to inpu data

- `r2 score (coefficeint of Dteremination` is measure of how well
the model has fit the input data. Its general range is [0,1] but
it can get negative values also.
- `r2_score = 1 - SS_res / SS_total` where
    - SS_total is the sum of squared differences b/w mean of target
    variable and target variable itself
    - SS_res is the sum of squared fiference b/w predicted and
    target variables
    - [Reference](https://en.wikipedia.org/wiki/Coefficient_of_determination)

## Resources
- [Practical ML](https://c.d2l.ai/stanford-cs329p/index.html)
- [Yannic kilcher](https://www.youtube.com/c/YannicKilcher/playlists)
- [Kaggler](https://www.youtube.com/channel/UCI8Y-po83Y4LLnIdAe_cmNA)
- [fastai](https://www.youtube.com/channel/UCX7Y2qWriXpqocG97SFW2OQ)

## Tools
### Pytorch lightning
- [Tensorboard in PT-L](https://learnopencv.com/tensorboard-with-pytorch-lightning/)

## Training techniques
### Learning rate finder
- [LR range test blogpost](https://sgugger.github.io/how-do-you-find-a-good-learning-rate.html)

### LR schedulers
- https://www.jeremyjordan.me/nn-learning-rate/
- [Cosine Annealing - Papers with code](https://paperswithcode.com/method/cosine-annealing)
- [Medium post on SGDR](https://towardsdatascience.com/https-medium-com-reina-wang-tw-stochastic-gradient-descent-with-restarts-5f511975163)

- With Higher learning rates, learning is faster (good until we start diverging)
- As we train longer, we tend to approach global minima, so need to reduce lr. Annealing is the part where we train with lower lr to find stable region (envisioned as plateau, where small changes in input doesnt lead to much change in loss function).
- Cyclic Learning rates - start from one end of sprectrum and increase / decrease the lr using a linear / exp / cosine like function
- warm restarts - Periodically Reseeting lr to lr_max helps us avoid `overfitting regions`, `saddle points`. Warm refers to the point that we continue to use the weights obtained after training for some time and not starting from some pre-defined initialization (random, zero etc)
- lr_max is found using the lr_range test proposed by Leslie Smith.
- Two major options
	- Cosine Annealing with warm restarts (Cosine is more aggressive annealing strategy)
	- One cycle lr (across the entire training cycle - linear / cosine annealing)
	- Generally One cycle lr is less over fitting than Cosine Annealing with warm restarts

- **Lower Batch size has a regulaizing effect (less generalization error); CON - higher training time**
- **SGD converges little slower but Adam is fast and overfits a litte**
- **SWA is a method to kinda average the model as it approaches minima, SGD often settles around the local minima but takes longer to find it**
- **Transformers work well - Attention is all you need paper**

### Optimizers
- [Comparison of different Optimizers and lr_schedulers](https://medium.com/vitalify-asia/whats-up-with-deep-learning-optimizers-since-adam-5c1d862b9db0)
- SGD with momentum and wieght decay, Warm restarts is generally SOTA, but takes more time to converge compared to Adam
- SGD with Stochastic Weighted averaging gives better results
- Adam converges faster but overfits lightly, different variants available -
- AdamW ???
- Ranger ???

### Image Augumentation techniques
- [Rand augument](https://github.com/ildoonet/pytorch-randaugment)
- [Cutmix, Mixup, gridmask kaggle post](https://www.kaggle.com/saife245/cutmix-vs-mixup-vs-gridmask-vs-cutout)
- [Cutmix and mixup on GPU/TPU by cdeotte](https://www.kaggle.com/cdeotte/cutmix-and-mixup-on-gpu-tpu)
- [GPU augumentations kaggle post](https://www.kaggle.com/c/flower-classification-with-tpus/discussion/132935)

## Validation strategy
### CV strategy
- [k-fold vs stratified kfold](https://www.google.com/search?q=when+to+use+kfold+and+when+to+use+stratified+k+fold&oq=when+to+use+kfold+and+when+to+use+stratified+k+fold&aqs=chrome..69i57.12117j0j1&sourceid=chrome&ie=UTF-8)
