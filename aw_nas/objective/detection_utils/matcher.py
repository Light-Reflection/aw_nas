import torch

from aw_nas.objective.detection_utils.base import Matcher
from aw_nas.utils import box_utils

__all__ = ["IOUMatcher"]


class IOUMatcher(Matcher):
    NAME = "iou_matcher"

    def __init__(self,
                 matched_threshold,
                 unmatched_threshold,
                 variance=(1., 1.),
                 schedule_cfg=None):
        super(IOUMatcher, self).__init__(schedule_cfg)
        self.matched_threshold = matched_threshold
        self.unmatched_threshold = unmatched_threshold
        self.variance = variance

    def __call__(self, boxes, labels, anchors):
        num_anchors = anchors.size(0)
        loc_t = torch.Tensor(1, num_anchors, 4)
        conf_t = torch.LongTensor(1, num_anchors)
        boxes = boxes.to(torch.float)
        widths = boxes[:, 2] - boxes[:, 0]
        heights = boxes[:, 3] - boxes[:, 1]
        if widths.min() == 0 or heights.min() == 0:
            idx = (widths > 0).__and__(heights > 0)
            boxes = boxes[idx]
            labels = labels[idx]
        if len(boxes) == 0:
            conf_t[0, :] = 0
            return conf_t.squeeze(0), loc_t.squeeze(0)
        if not isinstance(boxes, torch.Tensor):
            boxes = torch.tensor(boxes)
            labels = torch.tensor(labels)
        box_utils.match(self.matched_threshold, self.unmatched_threshold,
                        boxes.float(), anchors, self.variance, labels, loc_t,
                        conf_t, 0)
        loc_t = loc_t.squeeze(0)
        conf_t = conf_t.squeeze(0)
        return conf_t, loc_t
