"""Detector engine class"""
from torchvision.models import detection
import numpy as np
import torch
import cv2
from object_detector.coco_categories import get_categories
import warnings

# get rid of torch deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

# available models for torch.vision
RESNET = detection.fasterrcnn_resnet50_fpn
MOBILENET = detection.fasterrcnn_mobilenet_v3_large_320_fpn
RETINANET = detection.retinanet_resnet50_fpn

# what is considered as a car: car, truck, bus
CARS = [3, 6, 8]

# color for bounding boxes and text - blue
COLOR = [255, 0, 0]


class ImageError(Exception):
    """Exception class for errors when handling jpeg files"""
    pass


class Detector:
    """Detector class"""
    def __init__(self, net_model=RESNET, confidence=0.5):
        """Initialize detection model"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # get categories from file
        self.categories = get_categories()
        self.confidence = confidence
        self.image = None
        self.orig = None
        self.result = None
        self.model = net_model(pretrained=True,
                               progress=True,
                               pretrained_backbone=True).to(self.device)
        self.model.eval()

    def load_image(self, img_path):
        """Load image from >img_path< and prepare it for detection"""
        try:
            self.image = cv2.imread(img_path)
            width, height = self.image.shape[1], self.image.shape[0]
        except AttributeError as e:
            raise ImageError('Input image is missing!') from None
        # resize big images
        if width > 1200:
            dim = (1200, int((1200 / width) * height))
            self.image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        self.orig = self.image.copy()
        # process image for detection
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = self.image.transpose((2, 0, 1))
        self.image = np.expand_dims(self.image, axis=0)
        self.image = self.image / 255.0
        self.image = torch.FloatTensor(self.image)

    def run_detection(self):
        """Run detection.
         result dict:
        'count' - number of detections
        'boxes'  - list of bounding boxes
        'labels - list of labels for boxes"""
        # send image to the device
        self.image = self.image.to(self.device)
        # run detection
        detections = self.model(self.image)[0]
        # loop over detections
        result = dict(count=0, boxes=[], labels=[])
        count = 0
        for i in range(0, len(detections["boxes"])):
            confidence = detections["scores"][i]
            idx = int(detections["labels"][i])
            # when condition is met append to list of boxes and labels
            if idx in CARS and confidence > self.confidence:
                count += 1
                box = detections["boxes"][i].detach().cpu().numpy()
                result['boxes'].append(box.astype("int"))
                result['labels'].append(f"{self.categories[idx - 1]['name']} {confidence * 100:.2f}%")
        result['count'] = count
        self.result = result

    def get_result_image(self, img_path):
        """Draw boxes and put labels on the result image using result dict.
        Save result image to JPG file."""
        count = self.result['count']
        # loop over boxes and labels
        for box, label in zip(self.result["boxes"], self.result['labels']):
            (startX, startY, endX, endY) = box
            cv2.rectangle(self.orig, (startX, startY), (endX, endY),
                              COLOR, 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(self.orig, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2)
        title = f'Count: {count}'
        cv2.putText(self.orig, title, (0, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, COLOR, 3)
        # save result
        cv2.imwrite(img_path, self.orig)


if __name__ == '__main__':
    # test detector
    d = Detector()
    d.load_image('images/test_1.jpg')
    d.run_detection()
    d.get_result_image('images/result.jpg')
    print('Count: ', d.result['count'])
    print('Boxes: ', d.result['boxes'])
    print('Labels: ', d.result['labels'])

