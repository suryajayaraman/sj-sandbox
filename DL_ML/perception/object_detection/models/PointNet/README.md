
## [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://arxiv.org/abs/1612.00593)

- Proposes a new Deep Learning architecture that can directly work on Point cloud data and perform 
  Object classification and semantic segmentation tasks. 

- `Core idea` A symmetric function (max pooling layer) along with input and feature transformation
  techniques help classify and segment unordered point cloud data. 

- Performance compared againts benchmarks (MV-CNN, 3D CNN) etc, gives similar / better performance with 
  improvements in inference time, memory consumption. Has O(N) Linear space and time complexity. 

- Theoretical and empirical analysis of the proposed solution explained with intuition of the network 
  learnings via various visualisations - tSNE, Depth maps etc
