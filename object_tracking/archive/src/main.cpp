#include "eigen3/Eigen/Dense"
#include "sort/utils.h"
#include <iostream>

int main(int argc, char *argv[]) {
  // test inputs
  Eigen::MatrixXd bb1(4, 5);
  Eigen::MatrixXd bb2(3, 5);

  bb1 << 1, 7, 5, 6, 4, 3, 3, 7, 6, 7, 8, 4, 0, 3, 0, 0, 8, 0, 4, 3;

  bb2 << 0, 6, 0, 2, 5, 7, 7, 6, 0, 7, 5, 6, 7, 6, 4;

  std::cout << "iou = \n" << batchIoU(bb1, bb2) << "\n";
  return 0;
}
