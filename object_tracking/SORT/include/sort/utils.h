/**
 * @file utils.h
 * @author J Surya (suryajayaraman97@gmail.com)
 * @brief File contains utilities function to implement the
 * SORT algorithm. File contains C++ implementation of many of
 * functions in https://github.com/abewley/sort/blob/master/sort.py
 *
 * @version 0.1
 * @date 2022-05-02
 *
 * @copyright Copyright (c) 2022
 */

#ifndef _UTILS_H_
#define _UTILS_H_

#include "eigen3/Eigen/Dense" // for matrix operations
#include <iostream>           // printing to console

/**
 * @brief Structure containing placeholders for
 * storing data association function output
 */
struct associationOutput {
  // member variables
  Eigen::MatrixXi matchedIndices;
  Eigen::VectorXi unMatchedDets;
  Eigen::VectorXi unMatchedTracks;
};

/**
 * @brief Function computes element wise maximum / minimum
 * of vectors along rows / columns
 * @param vec1 (N,1) length column vector
 * @param vec2 (M,1) length column vector
 * @param maximum boolean flag to indicate whether to compute
 * element wise maximum or minimum
 * @return resultMtx (Eigen::MatrixXd)
 *
 * @example vec1 = [1, 3, 8, 0] and vec2 = [0, 7, 5]
 * Internally vec1 is populated as [[1, 1, 1],
 *                                  [3, 3, 3],
 *                                  [8, 8, 8],
 *                                  [0, 0, 0]])
 * and vec2 as  [0, 7, 5],
 *              [0, 7, 5],
 *              [0, 7, 5],
 *              [0, 7, 5]])
 * Element wise maximum comparison gives resultMtx as [[1, 7, 5],
 *                                                     [3, 7, 5],
 *                                                     [8, 8, 8],
 *                                                     [0, 7, 5]]))
 */
Eigen::MatrixXd compareVectors(const Eigen::VectorXd &vec1,
                               const Eigen::VectorXd &vec2,
                               const bool &maximum);

/**
 * @brief Function computes IOU between two bboxes given
 * in [x1,y1,x2,y2] form
 *
 * @param bb1 (M,5) array where M is number of bounding
 * boxes in bb1. 5 columns indicate [x1,y1,x2,y2,confidence]
 * @param bb2 (N,5) where N is number of bounding boxes in bb2.
 *
 * @return iou (Eigen::MatrixXd) (M,N) array containing intersection
 * over union for each combination of bounding boxes in bb1 and bb2
 *
 * @example bb1 shape = (7,5), bb2 shape = (6,5)
 * then return value will have shape = (7,6)
 */
Eigen::MatrixXd batchIoU(const Eigen::MatrixXd &bb1,
                         const Eigen::MatrixXd &bb2);

/**
 * @brief Converts a bounding box in the form [x1,y1,x2,y2, confidence]
 * to measurement z in the form [x,y,s,r] where x,y is the centre of
 * the box and s is the scale/area and r is the aspect ratio
 *
 * @param bbox (5,) vector representing bounding box
 * top left and bottom right x,y coordinates and confidence

 * @return Eigen::VectorXd - (4,1) measurement vector equivalent
 * to input bounding box
 */
Eigen::VectorXd bboxToMeas(const Eigen::VectorXd &bbox);

/**
 * @brief Converts a bounding box in the centre form [x,y,s,r] to
 * [x1,y1,x2,y2] form where x1,y1 is the top left and
 * x2,y2 is the bottom right coordinates
 *
 * @param meas (4,) vector representing bounding box
 * centre x,y coordinates and area and aspect ratio
 *
 * @return Eigen::VectorXd - (N,) vector representing bounding box
 * top left and bottom right x,y coordinates
 */
Eigen::VectorXd measToBbox(const Eigen::VectorXd &meas);

/**
 * @brief Function assigns detections to tracked object
 * (both represented as bounding boxes)
 *
 * @param dets (N,5) array where each row indicates detections in
 * [x1,y1,x2,y2,confidence] format
 * @param tracks (M,5) array where each row contains track states vector
 * @param iouThreshold minimum iou metric to consider as valid match
 * @param DAOutput placeholder to store funciton output params
 *
 * DAOutput-> matchedIndices = (M,2) array where each row contains
 * index of matched track and detection.
 *
 * DAOutput-> unMatchedDets = Vector containing indices of detections for
 * which no tracks was associated
 *
 * DAOutput-> unMatchedTracks = Vector containing indices of tracks for
 * which no detections was associated
 */
void associateDetsToTracks(const Eigen::MatrixXd &dets,
                           const Eigen::MatrixXd &tracks,
                           const double &iouThreshold,
                           associationOutput *DAOutput);

#endif // _UTILS_H_
