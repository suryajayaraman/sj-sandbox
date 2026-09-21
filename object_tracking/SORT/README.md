# SORT (Simple Online and Realtime Tracking)

## Overview
- C++ implementation of [SORT algorithm](https://arxiv.org/abs/1602.00763)
- SORT (Simple and online realtime tracking), as the name indicates, is a simple Real-time tracking algorithm, where detections from the previous and the current frame are associated using the Hungarian algorithm and the state of each track is estimated using a Kalman filter. The algorithm is simple, fast and effective for tracking multiple objects in real-time.
- Often used as a baseline for tracking multiple objects in real-time, SORT is a simple and effective algorithm that can be used in various applications such as surveillance, autonomous driving, and robotics.

![SORT Algorithm output](images/SORT_output.gif)

- The repo uses [Eigen library](https://eigen.tuxfamily.org/index.php?title=Main_Page) for matrix operations and [hungarian algorithm](../../fusion/hungarianAlgorithm/) implementation
- [sort.py](scripts/sort.py) from [official repo](https://github.com/abewley/sort) is the reference python implementation for this repo. Check the original repo on how to run the python script.

## Requirements
The code was developed on Ubuntu 20.04 LTS OS with
- g++ 9.4.0
- cmake 3.16.3
- Eigen 3.3
- OpenCV

## Reference Folder Structure
```
data/
    train/
        ADL-Rundle-6/
            det/det/txt
        ADL-Rundle-8/
            det/det.txt
        .....

mot_benchmark
    train/
        ADL-Rundle-6/
            det/det/txt
            gt/gt.txt
            img1/
                000001.jpg
                000002.jpg
                ......
```
- The `data/` folder contains necessary bounding box information for all frames in all scenarios
- The `mot_benchmark/` folder contains corresponding camera frames and is optional (~1.5GB download size)

## Results

### Python script runtime speed
![pyScriptRunTime](images/python_script_run_time_reference.png)

## References
- [SORT original paper](https://arxiv.org/abs/1602.00763)
- [SORT official github implementation](https://github.com/abewley/sort)
- [SORT cpp implementation](https://github.com/yasenh/sort-cpp)
- [SORT python implementation with importance to reidentification](https://github.com/danbochman/SORT)
