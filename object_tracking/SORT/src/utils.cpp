#include "sort/utils.h"

Eigen::MatrixXd compareVectors(const Eigen::VectorXd &vec1,
                               const Eigen::VectorXd &vec2,
                               const bool &maximum) {
  // assume vec1 shape = (4,1) and vec2 shape = (3,1)
  // initialize return matrix of size (4,3)
  Eigen::MatrixXd resultMtx(vec1.size(), vec2.size());

  // variables to populate vectors across rows / columns
  // In mat1, vec1 is repeated on each column
  // In mat2, vec2 is repeated on each row
  // mat1 shape = mat2 shape = (4,3).
  Eigen::MatrixXd mat1 = vec1.replicate(1, vec2.size());
  Eigen::MatrixXd mat2 = vec2.transpose().replicate(vec1.size(), 1);

  // compute element wise maximum / minimum
  if (maximum == true)
    resultMtx = mat1.array().max(mat2.array());
  else
    resultMtx = mat1.array().min(mat2.array());

  return resultMtx;
}

Eigen::MatrixXd batchIoU(const Eigen::MatrixXd &bb1,
                         const Eigen::MatrixXd &bb2) {
  // assume bb1 shape = (7,5) and bb2 shape = (6,5)
  // bb1Rows = 7 and bb2Rows = 6
  const std::size_t bb1Rows = bb1.rows();
  const std::size_t bb2Rows = bb2.rows();

  // initialize return variable
  Eigen::MatrixXd iou = Eigen::MatrixXd::Zero(bb1Rows, bb2Rows);

  // xx1, yy1 denote the x,y coordinates of left top
  // corner of intersection between the bounding boxes
  // xx1 shape = yy1 shape = (7,6)
  Eigen::MatrixXd xx1 = compareVectors(bb1.col(0), bb2.col(0), true);
  Eigen::MatrixXd yy1 = compareVectors(bb1.col(1), bb2.col(1), true);

  // xx2, yy2 denote the x,y coordinates of right bottom
  // corner of intersection between the bounding boxes
  // xx2 shape = yy2 shape = (7,6)
  Eigen::MatrixXd xx2 = compareVectors(bb1.col(2), bb2.col(2), false);
  Eigen::MatrixXd yy2 = compareVectors(bb1.col(3), bb2.col(3), false);

  // calculate the intersection area using width * height. wh  = (7,6)
  Eigen::MatrixXd w = (xx2 - xx1).cwiseMax(0.0);
  Eigen::MatrixXd h = (yy2 - yy1).cwiseMax(0.0);
  Eigen::MatrixXd wh = w.array() * h.array();

  // iou = intersection / union where
  // union = area(bb_test) + are(bb_gt) - intersection
  // bb1Area shape = bb2Area shape = iou shape = (7,6)
  Eigen::MatrixXd bb1Area =
      ((bb1.col(2) - bb1.col(0)).array() * (bb1.col(3) - bb1.col(1)).array())
          .matrix()
          .replicate(1, bb2Rows);

  Eigen::MatrixXd bb2Area =
      ((bb2.col(2) - bb2.col(0)).array() * (bb2.col(3) - bb2.col(1)).array())
          .matrix()
          .transpose()
          .replicate(bb1Rows, 1);
  iou = wh.array() / (bb1Area + bb2Area - wh).array();
  return iou;
}

Eigen::VectorXd bboxToMeas(const Eigen::VectorXd &bbox) {
  // w,h are scalar doubles
  double w = bbox(2) - bbox(0); // width of bbox
  double h = bbox(3) - bbox(1); // height of bbox

  // initialize return variable
  Eigen::Vector4d measurement;
  measurement(0) = bbox(0) + w / 2; // x-coordinate of centre of bbox
  measurement(1) = bbox(1) + h / 2; // y-coordinate of centre of bbox
  measurement(2) = w * h;           // s = bbox area
  measurement(3) = w / h;           // r = width to height aspect ratio
  return measurement;
}

Eigen::VectorXd measToBbox(const Eigen::VectorXd &meas) {
  // x[2] = (w*h), x[3] = (w/h)
  // w and h are scalar doubles
  double w = sqrt(meas(2) * meas(3));
  double h = meas(2) / w;

  // convert coordinates from centre to top left and bottom right
  // initialize return variable
  Eigen::Vector4d bbox;
  bbox(0) = meas(0) - w / 2;
  bbox(1) = meas(1) - h / 2;
  bbox(2) = meas(0) + w / 2;
  bbox(3) = meas(1) + h / 2;
  return bbox;
}

void associateDetsToTracks(const Eigen::MatrixXd &dets,
                           const Eigen::MatrixXd &tracks,
                           const double &iouThreshold,
                           associationOutput *DAOutput) {
  // assume tracks shape = (6,5), dets shape = (7,5)
  // means there are 6 tracks and 7 measurements

  // empty tracks scenario, return empty matched matrix
  // indices of all detections and tracks
  // if(tracks.rows() == 0)
  // {
  //     DAOutput->matchedIndices = Eigen::MatrixXi::Zero(0,2);
  //     DAOutput->matchedIndices = Eigen::VectorXi::LinSpaced(0, )
  //     DAOutput->matchedIndices = Eigen::MatrixXi::Zero(0,2);

  //     return np.empty((0,2),dtype=int), np.arange(len(detections)),
  //     np.empty((0,5),dtype=int)
  // }

  // else
  // {

  // }

  return;
}

//     # if not empty
//     else:
//     # find the overlap between bbox of tracks, measurements
//     # iou_matrix shape = (7,6) where each entry range = [0,1]
//     iou_matrix = iou_batch(detections, trackers)

//     # if at least there is one matched association
//     if min(iou_matrix.shape) > 0:

//         # ensure the returned matrix is valid by ensuring
//         # sum across every row and column sums to 1
//         # a shape = (7,6), int array containing 0s and 1s
//         a = (iou_matrix > iou_threshold).astype(np.int32)

//         # simple case where the overlap itself is enough to solve
//         # the data association problem, i.e there is only one 1 in
//         # each row / column. If so, directly stack the indices
//         if a.sum(1).max() == 1 and a.sum(0).max() == 1:

//             # store indices where iou matrix is greater than threshold
//             # and stack them row wise. eg : matched_indices shape = (6,2)
//             # means there are 6 track-detection association from iou_matrix
//             matched_indices = np.stack(np.where(a), axis=1)

//         else:
//         matched_indices = linear_assignment(-iou_matrix)
//     else:
//         matched_indices = np.empty(shape=(0,2))

//     # store indices of detections not associated to any track
//     unmatched_detections = []
//     for d, det in enumerate(detections):
//         if(d not in matched_indices[:,0]):
//         unmatched_detections.append(d)

//     # store indices of tracks not associated to any detection
//     unmatched_trackers = []
//     for t, trk in enumerate(trackers):
//         if(t not in matched_indices[:,1]):
//         unmatched_trackers.append(t)

//     # filter out matched with low IOU
//     # and store those entries too in ummatched_ lists
//     # matches shape = matched_indices shape = (6,2)
//     # unmatched_detections = list of indices of unassociated detections
//     # unmatched_trackers = list of indices of unassociated trackers
//     matches = []
//     for m in matched_indices:
//         if(iou_matrix[m[0], m[1]]<iou_threshold):
//         unmatched_detections.append(m[0])
//         unmatched_trackers.append(m[1])
//         else:
//         matches.append(m.reshape(1,2))
//     if(len(matches)==0):
//         matches = np.empty((0,2),dtype=int)
//     else:
//         matches = np.concatenate(matches,axis=0)

//     return matches, np.array(unmatched_detections),
//     np.array(unmatched_trackers)

// }
