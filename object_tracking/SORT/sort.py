"""
SORT: A Simple, Online and Realtime Tracker
Copyright (C) 2016-2020 Alex Bewley alex@bewley.ai

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# basic libraries import
import os
import glob
import time
import argparse
import numpy as np
from typing import Any, List

# plotting libraries import
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io

# KF library
from filterpy.kalman import KalmanFilter

# SET SEED TO GET REPRODUCIBLE RESULTLS
np.random.seed(0)


def linear_assignment(cost_matrix) -> np.ndarray:
    """Function solves the optimal assignment problem
    using Jonker-Volgenant algorithm for dense (LAPJV)
    matrices

    Args:
        cost_matrix (np.ndarray): (N,M) matrix where
        c_ij refers to cost b/w ith row and jth column
        elements

    Returns:
        np.ndarray : (P,2) where P = number of valid
        assignments which are optimal based on input
        cost matrix. eg : if cost matrix shape = (7,6),
        there are 7 rows for which 6 columns are
        to be assigned.

        Possible output = [[0,1]
                           [1,2]
                           [2,3]
                           [3,4]
                           [4,5]]
        means there are 5 valid assignments, 2nd column
        to 1st row, 3rd column to 2nd row and 4th column
        to 3rd row and so on
    """
    try:
        import lap

        _, x, y = lap.lapjv(cost_matrix, extend_cost=True)
        return np.array([[y[i], i] for i in x if i >= 0])  #
    except ImportError:
        from scipy.optimize import linear_sum_assignment

        x, y = linear_sum_assignment(cost_matrix)
        return np.array(list(zip(x, y)))


def iou_batch(bb_test: np.ndarray, bb_gt: np.ndarray) -> np.ndarray:
    """Computes IOU between two bboxes given in [x1,y1,x2,y2] form

    Args:
        bb_test (np.ndarray): (M,5) where M is number of bounding
        boxes in bb_test. 5 columns indicate [x1,y1,x2,y2,confidence].

        bb_gt (np.ndarray): (N,5) where N is number of bounding
        boxes in bb_gt.

    Returns:
        iou (np.ndarray) : (M,N) array containing intersection
        over union for each combination of bounding boxes in
        bb_test and bb_gt

    Example
      bb_test = (7,5) and bb_gt = (6,5), then return value
      will have shape = (7,6)
    """
    # assume bb_test shape = (7,5) and bb_gt shape = (6,5)

    # insert axis at 1st axis, bb_gt shape = (1,6,5)
    bb_gt = np.expand_dims(bb_gt, 0)

    # insert axis at 2nd axis, bb_gt shape = (7,1,5)
    bb_test = np.expand_dims(bb_test, 1)

    # xx1, yy1 denote the x,y coordinates of left top
    # corner of intersection between the bounding boxes
    # xx1 shape = yy1 shape = (7,6)
    xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])
    yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])

    # xx2, yy2 denote the x,y coordinates of right bottom
    # corner of intersection between the bounding boxes
    # xx2 shape = yy2 shape = (7,6)
    xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])
    yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])

    # calculate the intersection area using width * height
    # wh  = (7,6)
    w = np.maximum(0.0, xx2 - xx1)
    h = np.maximum(0.0, yy2 - yy1)
    wh = w * h

    # iou = intersection / union where
    # union = area(bb_test) + are(bb_gt) - intersection
    # iou shape = (7,6)
    iou = wh / (
        (bb_test[..., 2] - bb_test[..., 0]) * (bb_test[..., 3] - bb_test[..., 1])
        + (bb_gt[..., 2] - bb_gt[..., 0]) * (bb_gt[..., 3] - bb_gt[..., 1])
        - wh
    )
    return iou


def convert_bbox_to_z(bbox: np.ndarray) -> np.ndarray:
    """Converts a bounding box in the form [x1,y1,x2,y2, confidence]
     to measurement z in the form [x,y,s,r] where x,y is the centre of
     the box and s is the scale/area and r is the aspect ratio

    Args:
        bbox (np.ndarray): (5,) vector representing bounding box
        top left and bottom right x,y coordinates and confidence

    Returns:
        np.ndarray : (4,1) measurement vector equivalent to input
        bounding box
    """
    # w,h,x,y are scalar doubles
    w = bbox[2] - bbox[0]  # width of bbox
    h = bbox[3] - bbox[1]  # height of bbox
    x = bbox[0] + w / 2.0  # x-coordinate of centre of bbox
    y = bbox[1] + h / 2.0  # y-coordinate of centre of bbox
    s = w * h  # s = bbox area
    r = w / float(h)  # r = width to height aspect ratio
    return np.array([x, y, s, r]).reshape((4, 1))


def convert_x_to_bbox(x: np.ndarray, score: Any = None) -> np.ndarray:
    """Converts a bounding box in the centre form [x,y,s,r] to
      [x1,y1,x2,y2] form where x1,y1 is the top left and
      x2,y2 is the bottom right coordinates

    Args:
        x (np.ndarray): (4,) vector representing bounding box
        centre x,y coordinates and area and aspect ratio

        score (Any, optional): confidence of bbox. Defaults to None.
        If given, the value is given as such in output

    Returns:
        np.ndarray: (1,N) vector representing bounding box
        top left and bottom right x,y coordinates
        N = 4 if score is None
        N = 5 if score is not None
    """
    # x[2] = (w*h), x[3] = (w/h)
    # w and h are scalar doubles
    w = np.sqrt(x[2] * x[3])
    h = x[2] / w

    # convert coordinates from centre to top left and bottom right
    if score == None:
        return np.array(
            [x[0] - w / 2.0, x[1] - h / 2.0, x[0] + w / 2.0, x[1] + h / 2.0]
        ).reshape((1, 4))
    else:
        return np.array(
            [x[0] - w / 2.0, x[1] - h / 2.0, x[0] + w / 2.0, x[1] + h / 2.0, score]
        ).reshape((1, 5))


class KalmanBoxTracker(object):
    # static variable that keeps track of tracks initialized
    count = 0

    def __init__(self, bbox: np.ndarray) -> None:
        """This class represents the internal state of individual
        tracked objects observed as bbox.  Initialises a tracker
        using initial bounding box. State vector =
        [u,v,s,r,u_dot,v_dot,s_dot] as per SORT paper
        where u,v is centre of bbox, s = area of bbox,
        r = aspect ratio of bbox.

        Motion model is a constant velocity model and measurement
        model assumes [u,v,s,r] states are observed

        Args:
            bbox (np.ndarray): (5,) vector representing bounding box
            top left and bottom right x,y coordinates and confidence
        """
        # define constant velocity model
        self.kf = KalmanFilter(dim_x=7, dim_z=4)

        # transition matrix shape = (7,7)
        self.kf.F = np.array(
            [
                [1, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 1],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1],
            ]
        )

        # measurement matrix shape = (4,7)
        self.kf.H = np.array(
            [
                [1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
            ]
        )

        # measurement noise shape = (4,4)
        self.kf.R[2:, 2:] *= 10.0

        # state covariance shape = (7,7)
        # give high uncertainty to the unobservable initial velocities
        self.kf.P[4:, 4:] *= 1000.0
        self.kf.P *= 10.0

        # process noise shape = (7,7)
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[4:, 4:] *= 0.01

        # state is initialized to using input bbox
        self.kf.x[:4] = convert_bbox_to_z(bbox)

        # counter for incrementing track number
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1

        # these variables keep track of predicted states
        # when there's no measurement associated to this track
        self.time_since_update = 0
        self.history = []

        # hits = total number of detections associated with this track
        # hit_streak = number of consecutive frames where track is associated
        self.hits = 0
        self.hit_streak = 0
        self.age = 0

    def update(self, bbox: np.ndarray) -> None:
        """Performs Kalman filter update using observed bbox
        measurement to get posterior state and covariance
        Also resets tracker variables accordindly

        Args:
            bbox (np.ndarray): (5,) vector representing bounding box
            top left and bottom right x,y coordinates and confidence
        """
        # since the object's associated to a measurement,
        # reset history related varibles, containing predicted
        # states information
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1

        # convert bbox to [u,v,s,r] format and
        # perform kalman filter update
        self.kf.update(convert_bbox_to_z(bbox))

    def predict(self) -> np.ndarray:
        """Predicts state using constant velocity model
        and returns predicted state

        Returns:
            np.ndarray: predicted state vector
        """
        # if the old area + in delta_area equals 0
        # let delta_area be zero
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0

        # perform prediction
        self.kf.predict()
        self.age += 1

        # reset `updated` status, setting hit_streak
        # to 0 indicates, at least 1 timestamp has passed where
        # track hasn't been associated to a measurement
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1

        # keep track of predicted states, returning
        # the latest one
        self.history.append(convert_x_to_bbox(self.kf.x))
        return self.history[-1]

    def get_state(self) -> np.ndarray:
        """Function returns the current bounding box estimate
        Returns:
            np.ndarray: most recent estimate of target bbox in
            [x1,y1,x2,y2] format
        """
        return convert_x_to_bbox(self.kf.x)


def associate_detections_to_trackers(
    detections: np.ndarray, trackers: np.ndarray, iou_threshold: float = 0.3
) -> List[Any]:
    """Assigns detections to tracked object (both represented as bounding boxes)

    Args:
        detections (np.ndarray): (N,5) array where each row indicates detections in
        [x1,y1,x2,y2,confidence] format
        trackers (np.ndarray): (M,5) array where each row contains track states vector
        iou_threshold (float, optional): minimum iou metric to consider as
        valid match. Defaults to 0.3.

    Returns:
        matches, unmatched_detections and unmatched_trackers (List[Any]):
        matches = (M,2) array where each row contains index of matched
        track and detection.

        unmatched_detections - list containing indices of detections for
        which no tracks was associated

        unmatched_trackers - list containing indices of tracks for
        which no detection was associated
    """
    # assume trackers shape = (6,5), detections shape = (7,5)
    # means there are 6 tracks and 7 measurements

    # empty tracks scenario, return empty matched matrix
    # indices of all detections and tracks
    if len(trackers) == 0:
        return (
            np.empty((0, 2), dtype=int),
            np.arange(len(detections)),
            np.empty((0, 5), dtype=int),
        )

    # if not empty
    else:
        # find the overlap between bbox of tracks, measurements
        # iou_matrix shape = (7,6) where each entry range = [0,1]
        iou_matrix = iou_batch(detections, trackers)

        # if at least there is one matched association
        if min(iou_matrix.shape) > 0:
            # ensure the returned matrix is valid by ensuring
            # sum across every row and column sums to 1
            # a shape = (7,6), int array containing 0s and 1s
            a = (iou_matrix > iou_threshold).astype(np.int32)

            # simple case where the overlap itself is enough to solve
            # the data association problem, i.e there is only one 1 in
            # each row / column. If so, directly stack the indices
            if a.sum(1).max() == 1 and a.sum(0).max() == 1:
                # store indices where iou matrix is greater than threshold
                # and stack them row wise. eg : matched_indices shape = (6,2)
                # means there are 6 track-detection association from iou_matrix
                matched_indices = np.stack(np.where(a), axis=1)

            else:
                matched_indices = linear_assignment(-iou_matrix)
        else:
            matched_indices = np.empty(shape=(0, 2))

        # store indices of detections not associated to any track
        unmatched_detections = []
        for d, det in enumerate(detections):
            if d not in matched_indices[:, 0]:
                unmatched_detections.append(d)

        # store indices of tracks not associated to any detection
        unmatched_trackers = []
        for t, trk in enumerate(trackers):
            if t not in matched_indices[:, 1]:
                unmatched_trackers.append(t)

        # filter out matched with low IOU
        # and store those entries too in ummatched_ lists
        # matches shape = matched_indices shape = (6,2)
        # unmatched_detections = list of indices of unassociated detections
        # unmatched_trackers = list of indices of unassociated trackers
        matches = []
        for m in matched_indices:
            if iou_matrix[m[0], m[1]] < iou_threshold:
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1, 2))
        if len(matches) == 0:
            matches = np.empty((0, 2), dtype=int)
        else:
            matches = np.concatenate(matches, axis=0)

        return matches, np.array(unmatched_detections), np.array(unmatched_trackers)


class Sort(object):
    def __init__(
        self, max_age: int = 1, min_hits: int = 3, iou_threshold: float = 0.3
    ) -> None:
        """Sets parameters for SORT algorithm to setup Multi-Object
        Tracker. The tracker computes data association using hungarian
        algorithm on intersection over union (IoU) b/w bboxes of
        consecutive frames.

        `self.trackers = List[KalmanBoxTracker] represents list of tracked objects`

        Args:
            max_age (int, optional): Number of frames to consider when object is
            not detected. Defaults to 1.
            min_hits (int, optional): Number of frames to consider a track as confirmed. Defaults to 3.
            iou_threshold (float, optional): threhsold to consider a detection-track
            pair as valid association. Defaults to 0.3.
        """
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.frame_count = 0

        # placeholder for keeping list of tracks
        self.trackers = []

    def update(self, dets: np.ndarray = np.empty((0, 5))) -> np.ndarray:
        """Function updates internal set of tracks using input measurements.
        This function must be called once for each frame. Returns the a similar
        array, where the last column is the object ID.

        NOTE:
        1. The number of objects returned may differ from the number of detections provided.
        2. For frames without detections, empty array (use np.empty((0, 5)) must be passed

        Args:
            dets (np.ndarray, optional): (N,5) array of detections
            in the format [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...].
            Defaults to np.empty((0, 5)).

        Returns:
            np.ndarray: (M,5) where each row contains [x1,y1,x2,y2,trackID]
            of a confirmed object
        """
        self.frame_count += 1

        # assume self.trackers = (6,) length list
        # placeholder to store get predicted locations
        # from existing trackers. trks shape = (6,5)
        trks = np.zeros((len(self.trackers), 5))

        # placeholder for indices of tracks to be deleted
        to_del = []

        # iterate through existing tracks and
        # predict each independently. If any track goes
        # out of FOV, consider it to be deleted
        for t, trk in enumerate(trks):
            pos = self.trackers[t].predict()[0]
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            if np.any(np.isnan(pos)):
                to_del.append(t)

        # filter only rows containing full of valid entries
        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))

        # remove tracks deleted tracks from list
        for t in reversed(to_del):
            self.trackers.pop(t)

        # associate tracks to measurements
        # matched = (N,2) where 1st column indicates row index
        # and 2nd column indicates associated column index.
        # unmatched_dets = (M,) length list containing indices of unassociated detections
        # unmatched_trks = (P,) length list containing indices of unassociated tracks
        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(
            dets, trks, self.iou_threshold
        )

        # update matched trackers with assigned detections
        for m in matched:
            self.trackers[m[1]].update(dets[m[0], :])

        # create and initialise new trackers for unmatched detections
        for i in unmatched_dets:
            trk = KalmanBoxTracker(dets[i, :])
            self.trackers.append(trk)

        # initialize return variable, list of confirmed tracks.
        ret = []
        i = len(self.trackers)

        # iterate through existing tracks
        for trk in reversed(self.trackers):
            # d = (4,) length vector containing [x1,y1,x2,y2]
            # bbox coordinates
            d = trk.get_state()[0]

            # Conditions for track to be confirmed
            # 1. associated to detection in latest frame
            # 2. hit_streak >= min_hits
            if (trk.time_since_update < 1) and (
                trk.hit_streak >= self.min_hits or self.frame_count <= self.min_hits
            ):
                ret.append(
                    np.concatenate((d, [trk.id + 1])).reshape(1, -1)
                )  # +1 as MOT benchmark requires positive
            i -= 1

            # remove dead tracklet
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)

        # return stacked tracks of shape (M,5)
        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0, 5))


def parse_args() -> argparse.ArgumentParser:
    """Parse input arguments from CLI
    Returns:
        argparse.ArgumentParser: object with input arguments
    """
    parser = argparse.ArgumentParser(description="SORT demo")
    parser.add_argument(
        "--display",
        dest="display",
        help="Display online tracker output (slow) [False]",
        action="store_true",
    )
    parser.add_argument(
        "--seq_path", help="Path to detections.", type=str, default="data"
    )
    parser.add_argument(
        "--phase", help="Subdirectory in seq_path.", type=str, default="train"
    )
    parser.add_argument(
        "--max_age",
        help="Maximum number of frames to keep alive a track without associated detections.",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--min_hits",
        help="Minimum number of associated detections before track is initialised.",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--iou_threshold", help="Minimum IOU for match.", type=float, default=0.3
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    # parse CL arguments
    args = parse_args()
    display = args.display
    phase = args.phase

    # temporary variables
    total_time = 0.0
    total_frames = 0
    colours = np.random.rand(32, 3)  # used only for display

    # if display = true
    #   1. check if images exist
    #   2. create figure handles
    if display:
        if not os.path.exists("mot_benchmark"):
            print(
                "\n\tERROR: mot_benchmark link not found!\n\n    Create a symbolic link to the MOT benchmark\n    (https://motchallenge.net/data/2D_MOT_2015/#download). E.g.:\n\n    $ ln -s /path/to/MOT2015_challenge/2DMOT2015 mot_benchmark\n\n"
            )
            exit()
        plt.ion()
        fig = plt.figure()
        ax1 = fig.add_subplot(111, aspect="equal")

    # create output directory if not already exists
    if not os.path.exists("output"):
        os.makedirs("output")

    # pattern = path to folder containing detection text files for the
    # folder structure
    # seq_path (data/)
    #     phase (train/)
    #         pattern (ADL-Rundle-6/)
    #             det/det.txt
    #         pattern (ADL-Rundle-8/)
    #             det/det.txt
    #         ..........
    pattern = os.path.join(args.seq_path, phase, "*", "det", "det.txt")

    # iterate through each folder
    for seq_dets_fn in glob.glob(pattern):
        # create SORT Tracker object with input arguments
        mot_tracker = Sort(
            max_age=args.max_age,
            min_hits=args.min_hits,
            iou_threshold=args.iou_threshold,
        )

        # load detections for scenario as np array
        # seq_dets = (N,10) array in MOT benchmark format.
        # <frame_no, id, bbx, bby, bbw, bbh, conf, x, y, z>
        # The number of frames M is lesser compared to number of
        # detection N because there can be many objects in single frame
        seq_dets = np.loadtxt(seq_dets_fn, delimiter=",")

        # seq is string = name of scenario. eg: ADL-Rundle-6
        seq = seq_dets_fn[pattern.find("*") :].split(os.path.sep)[0]

        # file handle for writing output
        with open(os.path.join("output", "%s.txt" % (seq)), "w") as out_file:
            print("Processing %s." % (seq))

            # iterate through each frame in scenario
            for frame in range(int(seq_dets[:, 0].max())):
                # detection and frame numbers begin at 1
                frame += 1

                # filter detections belonging to this frame
                # dets = (P,5) where P = number of detections in that frame
                dets = seq_dets[seq_dets[:, 0] == frame, 2:7]

                # convert to [x1,y1,w,h] to [x1,y1,x2,y2]
                dets[:, 2:4] += dets[:, 0:2]
                total_frames += 1

                # show corresponding image if display = true
                if display:
                    fn = os.path.join(
                        "mot_benchmark", phase, seq, "img1", "%06d.jpg" % (frame)
                    )
                    im = io.imread(fn)
                    ax1.imshow(im)
                    plt.title(seq + " Tracked Targets")

                # Call tracker update fn with latest measurements to get list
                # of tracked objects. trackers = (T,5) in [x1,y1,x2,y2,id] format
                start_time = time.time()
                trackers = mot_tracker.update(dets)
                cycle_time = time.time() - start_time
                total_time += cycle_time

                # write output to file
                for d in trackers:
                    print(
                        "%d,%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1"
                        % (frame, d[4], d[0], d[1], d[2] - d[0], d[3] - d[1]),
                        file=out_file,
                    )
                    if display:
                        d = d.astype(np.int32)
                        # indicate bbox of tracked object
                        ax1.add_patch(
                            patches.Rectangle(
                                (d[0], d[1]),
                                d[2] - d[0],
                                d[3] - d[1],
                                fill=False,
                                lw=3,
                                ec=colours[d[4] % 32, :],
                            )
                        )

                if display:
                    fig.canvas.flush_events()
                    plt.draw()
                    ax1.cla()

    print(
        "Total Tracking took: %.3f seconds for %d frames or %.1f FPS"
        % (total_time, total_frames, total_frames / total_time)
    )

    if display:
        print("Note: to get real runtime results run without the option: --display")
