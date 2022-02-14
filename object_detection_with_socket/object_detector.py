#-*-coding:utf-8-*-
import numpy as np
import torch
import torchvision
from torchvision.models import detection

#copied from official pytorch web
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

class ObjectDetector(object):
    def __init__(self):
        device =("cuda:0" if torch.cuda.is_available() else "cpu")
        print("model is on device:{}".format(device))
        self.device = device

        self.model = detection.fasterrcnn_mobilenet_v3_large_320_fpn(pretrained=True)
        self.model.to(device)
        self.model.eval()

        self.mean = torch.Tensor([0.485, 0.456, 0.406])
        self.std = torch.Tensor([0.229, 0.224, 0.225])

    def label2cat(self, x):
        return COCO_INSTANCE_CATEGORY_NAMES[x]

    def __call__(self, x):
        """
        x: (H, W, C) input image
        """
        #normalize
        input = torch.Tensor(np.asarray(x, dtype=np.float32) / 255.).permute(2, 0, 1) #(C, H, W)
        input = (input - self.mean[:, None, None]) / self.std[:, None, None]

        input = input.unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.model(input)

        return out[0]


if __name__ == "__main__":
    object_detector = ObjectDetector()
    x = np.ones((320, 320, 3), dtype=np.uint8)
    output = object_detector(x)
    print(output)
