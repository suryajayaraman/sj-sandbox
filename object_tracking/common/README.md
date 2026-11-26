# Common Object tracking topics

## Ablation studies
- Ablate detector confidence. Compare Box Tracking vs. Mask Tracking. Analyze failure cases (occlusion, missed detections).

## Metrics

### Standard MOT metrics
- MOTA(↑): Multi-object tracking accuracy
- MOTP(↑): Multi-object tracking precision
- FAF(↓): number of false alarms per frame. = sum (FP) / total_frames. (normalized value; %).
- MT(↑): number of mostly tracked trajectories. I.e. target has the same label for at least 80% of its life span. (normalized value; %)
- ML(↓): number of mostly lost trajectories. i.e. target is not tracked for at least 20% of its life span. (normalized value; %)
- FP(↓): number of false detections.
- FN(↓): number of missed detections.
- ID sw(↓): number of times an ID switches to a different previously tracked object.
- Frag(↓): number of fragmentations where a track is interrupted by a missed detection.

- 3 cases where ID sw and Frag might be affected
    - Drop out without ID swap (an object is occluded and the tracker fails to track it) - affects Frag
    - ID swap without Dropout (two or more objects cross each other, after which IDs are swapped) - affects ID sw
    - Dropout with new ID.  A track is lost and later re-assigned a different ID. This can trigger both Fragmentation (trajectory interruption) and an IDSW (change in predicted ID for that ground truth target).

Evaluation measures with (↑), higher scores denote better performance; while for evaluation measures with (↓), lower scores denote better performance

### Temporally local metrics
- [Temporally local metrics for MOT](https://github.com/google-research/localmot)
- mAP, MOTA, IDF1, HOTA, ID switches
