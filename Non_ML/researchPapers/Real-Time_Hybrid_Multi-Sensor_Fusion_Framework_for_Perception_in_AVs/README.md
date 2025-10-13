# Real-Time Hybrid Multi-Sensor Fusion Framework for Perception in Autonomous Vehicles

[Link to Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6833089/pdf/sensors-19-04357.pdf)

## Objective

The paper presents a framework to perceive the environment through:
- Drivable space estimation
- Object state estimation by fusing data from LiDAR, Camera, and RADAR sensors

The algorithm is designed for real-time implementation on embedded devices while maintaining accuracy comparable to benchmark models. The "hybrid" approach comes from running two parallel algorithms:

1. Camera + LiDAR fusion for:
   - Road segmentation
   - Object detection
2. LiDAR + RADAR fusion for:
   - Obstacle detection
   - State tracking

The results from both pipelines are overlaid to create a comprehensive environmental perception.

## Obstacle Detection using LiDAR Data

LiDAR provides Point Cloud Data (PCD), delivering accurate and dense environmental information (millions of points per second). The processing pipeline includes:

1. Downsampling using Voxel grid
2. Filtering points outside Region of Interest (ROI) such as buildings
3. Segmentation into road and obstacle points:
   - Uses RANSAC algorithm
   - Road points treated as inliers
   - Obstacle points treated as outliers
4. Clustering:
   - Groups obstacle points based on Euclidean distance
   - Assigns points to clusters
   - Calculates cluster coordinates as mean of assigned points

## Role of Non-linear Kalman Filters

Kalman Filter (KF) serves as a state estimation algorithm with the following characteristics:

- Fuses data from multiple sensors (LiDAR and RADAR) to improve state estimates (2D position and velocities)
- Based on linear prediction and measurement models with Gaussian distributions
- Handles non-linear real-world systems through approximations
- Processes RADAR measurements in polar coordinates while maintaining state variables in Cartesian space
- Uses linear approximation (Jacobian of measurement model at recent state estimates) for state updates

Advanced variants include:
- Unscented Kalman Filter (UKF)
- Cubature Kalman Filter (CKF)
  
These variants use sigma point methods to approximate the distribution rather than the model itself, providing better results for highly non-linear cases at increased computational cost.