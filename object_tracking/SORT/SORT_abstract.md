## ABSTRACT
- Focus is to associate objects efficiently for online and realtime applications
- `Detection quality` = key factor influencing tracking performance, where changing the detector can improve tracking by up to **18.9%**
- `Kalman Filter + Hungarian algorithm` for the tracking components, this
approach achieves an accuracy comparable to SOTA online trackers.
- Tracker updates at a rate of 260 Hz, 20x other SOTA trackers


## 1 INTRODUCTION
- Online tracking where only detections from the previous and the current frame are presented to the tracker.
- MOT = data association problem where the aim is to associate detections across frames in a video sequence by `modelling the motion and appearance of objects` in the scene
- Appearance features beyond the detection component are ignored in tracking and only the bounding box position and size are used for both motion estimation and data association.
- Issues regarding short-term and long-term occlusion are also ignored,
as they occur very rarely and their explicit treatment introduces complexity
- Only pedestrians are tracked
- `CNN based detection in the
context of MOT`

## 2 LITERATURE SURVEY
- `MHT` and `JPDA` used traditionally, but have `exponential complexity` in dynamic environments
- Efficient JPDA using modern integer solvers
- MHT graph pruning techniques tried, still the methods are slow to be realtime
- **When considering only one-to-one correspondences modelled as bi-partite graph matching, globally optimal solutions such as the Hungarian algorithm are used**


## 3 METHODOLOGY

### 3.1 Detection
- `Faster RCNN model` to detect objects in environment
- 2 variants, namely the `ZF` version and `VGG16` based versions are compared using PASCAL VOC dataset.
- Detections consists of `pedestrian class alone with probability > 50%`
- **FrRCNN(VGG16) = best detector**, the best detector gives best tracking results for the previous SOTA method and SORT method


### 3.2 Estimation model
- Motion model used to propagate a target’s identity into the next frame.
- `Approximate the inter-frame displacements of
each object with a linear constant velocity model` which is independent of other objects and camera motion.
- `x = [u, v, s, r, u̇, v̇, ṡ]`

where

    - u = horizontal pixel location of the centre of the target bb
    - v = vertical pixel location of the centre of the target bb
    - s = scale (area) of targets's bb
    - r = aspect ratio of target's bb (assumed constant)

- When a detection is associated to a target, the detected bounding box is used to update the target state where the velocity components are solved optimally via a Kalman
filter framework.
- If no detection is associated to the tar-
get, its state is simply predicted without correction using the linear velocity model.


### 3.3 Data Association

- `The assignment cost matrix is computed as the intersection-over-union (IOU) distance
between each detection and all predicted bounding boxes
from the existing targets, solved using the Hungarian algorithm`
-  A minimum IOU is imposed to reject assignments where the detection to target overlap is less than IOU min.

- `IOU distance of the bounding boxes
implicitly handles short term occlusion caused by passing targets`
- When a target is covered by an occluding
object, only the occluder is detected. This allows both the occluder target to be corrected with the detec-
tion while the covered target is unaffected as no assignment is made

### 3.4 Creation and Deletion of Track Identities

- Unique identities need to be created or destroyed  when objects enter and leave the image.

`Track Initialization`
- Any detection with an overlap < IOU_min -> probability of an untracked object.
- Tracker is initialised using the geometry of the bounding box with the velocity = 0.
- As velocity = unobserved, large variance initializaiton for velocity
- Probationary period for new tracker, where detections need to be assoicated to prevent tracking of
false positives.


`Track termination`
- `Tracks Terminated if they are not detected for T_Lost
frames`. It prevents exp.growth in the num of tracks caused by long durations of just prediction and no correction
- `T_Lost = 1` because:
    - cv = poor predictor
    - onot bothered about object re-identification

- Early deletion of lost targets -> **&uarr;**  efficiency. If an object reappears, tracking will implicitly resume under a new identity.



## 4 EXPERIMENTS
- Test set of MOT2015 benchmark dataset
- Kalman filter covariances, IOU_min, and T_Lost parameters, tuned on validation.
- FrRCNN(VGG16) = detection model


### 4.1 Metrics
- MOTA(↑): Multi-object tracking accuracy
- MOTP(↑): Multi-object tracking precision
- FAF(↓): number of false alarms per frame.
- MT(↑): number of mostly tracked trajectories. I.e. target has the same label for at least 80% of its life span.
- ML(↓): number of mostly lost trajectories. i.e. target is not tracked for at least 20% of its life span.
- FP(↓): number of false detections.
- FN(↓): number of missed detections.
- ID sw(↓): number of times an ID switches to a different previously tracked object.
- Frag(↓): number of fragmentations where a track is in-
terrupted by miss detection.

`Evaluation measures with (↑), higher scores denote better performance; while for evaluation measures with (↓), lower scores denote better performance`


### 4.2 Performance Evaluation
- SORT = highest MOTA score for the online trackers
- As SORT focusses on frame-to-frame associations, the number of lost targets (ML) is minimal and the low-
est number of lost targets.


### 4.3 Runtime
- `260 Hz on single core of an Intel i7 2.5GHz machine with 16 GB memory`
