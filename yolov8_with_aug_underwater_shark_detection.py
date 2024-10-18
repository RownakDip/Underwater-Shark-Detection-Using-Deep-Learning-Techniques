# -*- coding: utf-8 -*-
"""Yolov8  with aug underwater-SHARK-detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Dr6iszwdVTO9GdXP8U1EBQdXkZXHkfB3
"""

!nvidia-smi

!pip install ultralytics
!pip install albumentations

from ultralytics import YOLO
import os
from IPython.display import display, Image
from IPython import display
display.clear_output()
!yolo checks

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="6RW5BXL4z1TBKvr2WJeB")
project = rf.workspace("fyp-b7z9h").project("underwater-species-detection-on-bruvs")
version = project.version(4)
dataset = version.download("yolov8")

import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
# Import the torch module
import torch

# Define the transformation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=40, p=0.7),
    A.Blur(blur_limit=3, p=0.1),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

class UnderwaterDataset(torch.utils.data.Dataset):
    def __init__(self, img_dir, annotations):
        self.img_dir = img_dir
        self.annotations = annotations

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.annotations[idx]['image'])
        image = cv2.imread(img_path)

        # Apply the preprocessing transform here
        augmented = transform(image=image)
        return augmented['image'], self.annotations[idx]['label']

!yolo task=detect mode=train model=yolov8m.pt data=/content/Underwater-Species-Detection-on-BRUVs-4/data.yaml epochs=20 imgsz=640 augment=True

Image(filename=f'/content/runs/detect/train6/confusion_matrix.png')

Image(filename=f'/content/runs/detect/train6/results.png', width=600)

!yolo task=detect mode=val model=/content/runs/detect/train6/weights/best.pt data=/content/Underwater-Species-Detection-on-BRUVs-4/data.yaml

!yolo task=detect mode=predict model=/content/runs/detect/train6/weights/best.pt source=/content/Underwater-Species-Detection-on-BRUVs-4/test/images

!ls runs/detect/predict

from IPython.display import Image, display

# Replace 'predicted_image.jpg' with the actual file name from predict2 folder
display(Image(filename='/content/runs/detect/predict/LT003_GP010011_0721-A-5-_png.rf.ff1568052564e52dc2c8b622d0cd8442.jpg'))

import os
import random
from IPython.display import Image, display

# Define the path to the folder
image_folder = 'runs/detect/predict/'

# List all files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

# Select 5 random images from the list
random_images = random.sample(image_files, 5)

# Display the random images
for image_file in random_images:
    display(Image(filename=os.path.join(image_folder, image_file)))