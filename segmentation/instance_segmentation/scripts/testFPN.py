import torch
import torchvision
from torchvision.ops.feature_pyramid_network import LastLevelMaxPool

from collections import OrderedDict


if __name__ == "__main__":
    model = torchvision.ops.FeaturePyramidNetwork(
        [10, 20, 30], 5, extra_blocks=LastLevelMaxPool()
    )

    x = OrderedDict()
    x["feat0"] = torch.rand(1, 10, 64, 64)
    x["feat1"] = torch.rand(1, 20, 16, 16)
    x["feat2"] = torch.rand(1, 30, 8, 8)
    preds = model(x)
