# [BDD100K dataset](https://arxiv.org/pdf/1805.04687)

## Abstract
- Released in Apr 2020
- Video dataset, containing 100K videos and 10k tasks to evaluate
- Contains geographic, einvronment, and weather diversity
- Benchmark for multi-task learning

## Introduction
- Existing datasets limited in scene variation, richness of annotations, geographic distribution
- Dataset overfitting
- Difficult to annotate for instance segmentation, multi object tracking and segmentation tasks
- Suitable for following tasks (heterogenous tasks - meaning, tasks that produce different output formasts)
    - Image tagging
    - Lane detection
    - Drivable area segmentation
    - road object detection
    - semantic segmentation
    - instance segmentation
    - multi object detection tracking
    - multi object segmentation tracking
    - domain adaptation
    - imitation learning

## Related works
- Same places as [Berkley DeepDrive dataset](http://bdd-data.berkeley.edu/), but for heterogenous task learning

### Multi-task learning
- Improves generalization of tasks by learning from other tasks
- Homogenous task learning - same output structure (eg: pixle level prediction) for all tasks invovled
- Heteregenous task learning - different output sttructreu - point base, region based, temporal prediction

## BDD100k
- Crowd sourced from drivers, from different cities (NY, SF Bay Area etc) in US, using [Nexar kits](https://www.getnexar.com/)
- 720p resolution images, at 30fps, GPS, IMU recordings
- 100k videos, 40s each, collected from 50k rides
- 10th frame in each video is annotated for image tasks, while entire video is annotated for tracking tasks (NOTE: not all videos are annotated for tracking)

### Image Tagging
- Image annotations on six weather conditions (including snow, rain), 3 distinct times of day
- Equal number of daytime and night time videos

### Object Detection
- 10 categories for 100k images. Each annotation includes visibility attributes - occluded, truncated

### Lane Marking
- 8 categories - road curb, cross walk, double white, double yellow, double other color, single white, single yellow, singleo other color
- `other categories` are ignored during evaluation
- Additional attribute - continuty (full or dashed) and direction (parallel vs perpendicular)

### Drivable Area
- `Directly driveable area` - current lane, and where driver has right of way
- `Alternative driveable area` - adjacent lane, need to change lanes
- In cities streets, highways, where traffic is regulated, driveable area is within lane, and don't overlap with vehicles / objects
- In residential aarea, lanes are sparse

### Semantic Instance segmentation
- Instance segmentation for reference image in 10k videoes, randomly sampled from dataset
- Many clkasses (eg: sky) are not amenable to be split into instances, only small categories are assigned identifiers
- 40 classes; train/val/test split = 7k/1k/2k videos

### Multiple object tracking
- 2k videos + 40 seconds per video + 5 fps => 2000 x 40 x 5 = 400k frames
- Video has more diversity across wedather conditions and locations
- Distributions of box size (root of wh); ratio of max box size vs min box size; track length
- Occlusion and reappearing pattern

### Multiple Object Tracking and Segmentation
- Tracking and Segmentation with 90 videos (60 / 10/ 20 videos)
- Not as big as Video datasets (VOS)

### Imitattion learnings
- GPS, IMU data for visual input alongside driving trajectories

## Diversity
Two experiments on object detection and semantic segmentation

### Object detection
- When Objecte detection models are trained within subsets of dataset (city vs non city, day vs night), significant deviations in results observed

### Semantic Segmentation
- CityScapes colelcted in German cities, while BDD100k is in US cities
- Model trained in one dataset, doesn't perform well in other dataset - indicating domain gap.

## Multi-task learning
Explored ways to use low level annotations (image based) for complicated tasks (multi object tracking and segmentation)

 ### Homogenous Multitask learning
 - Effect of jointly training l


