
## ABSTRACT
SORT is a simple, pragmatic approach to real time tracking. This paper focusses on adding appearnac einformation to improve performance. Result is better performance when objects are occluded. The new approach invovles learninga  deep association metrics on large scale person re-idetnfication dataset. During online operation, measurement to track associations are established suing nearest neighbour quereis in visual appearance space. Results show 45% reduction in identity switches

## INTRODUCTION
- Tracking by detection was the best approach (at least in Mar 2017, when Fast-RCNN was SORT OD model)
- Other Frame-Frame tracking appraoches included classical approaches like JPDA (weighted sum of hypothesis) and MHT (multiple hypothesis maintained). But implementation and compute complexity make it not suitable for real time.
- SORT is simple approach which makes use of Kalman filtering in image space, and frame-frame association using Hungarian algorithm, with an association metric, that measures bounding box overlap.
- SORT + SOTA detector >  MHT + standard detectors.
- Overall tracking precision and accuracy for SORT is good, but Identity switching results are poor.
- Reason
    - association metric just measures bounding box overlap. So, it works well, when we have less uncertainty in state.
    - Hence, SORT has issues dealing with occlusions, which is common in frontal-view cameras.
- This paper tries to fix this, by using a more informed metric, that combines both motion and appearance information.
- Authors trained a separate CNN model, to discriminate pedestrians on large scale pedestrian re-identification dataset. Integrating this network increases the robustness of the algorithm against misses and occlusions.

## SORT WITH DEEP ASSOCIATION METRIC
- Conventional single hypothesis trackinng with recursive Kalman filters and frame-frame data assocaiation

### Track Handling and State Estimation
- Mostly identical to original SORT algorithm.
- **Assume camera is uncalibrated and don't consider ego motion information. Hence object movement in image space due to eeog-motion is not modelled (ideally should increase the uncertainty accordingly in process model), but this was the norm for all MOT benchmarks**
- State vector = [u, v, r, h, x_dot, y_dot, r_rot, h_dot]
    - (x,y) = bounding box center position
    - r = aspect ratio
    - h = height of bounding box
- `Constant velocity motion model` in image space
- Measurement z = [u, v, r, h]


### Assignment problem
