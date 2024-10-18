# -*- coding: utf-8 -*-
"""yoloV11_aug.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-M2_aQhHp9bbojCqBJM5jt3h8LNbGkP_
"""

!nvidia-smi

!pip install ultralytics

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
dataset = version.download("yolov11")

dataset.location

!yolo task=detect mode=train model=yolo11s.pt data={dataset.location}/data.yaml epochs=20 imgsz=640 plots=True augment=True

from IPython.display import Image as IPyImage
IPyImage(filename=f'/content/runs/detect/train12/confusion_matrix.png')

!yolo task=detect mode=val model=/content/runs/detect/train12/weights/best.pt data=/content/Underwater-Species-Detection-on-BRUVs-4/data.yaml

Image(filename=f'/content/runs/detect/train12/results.png', width=600)

!yolo task=detect mode=val model=/content/runs/detect/train12/weights/best.pt data=/content/Underwater-Species-Detection-on-BRUVs-4/data.yaml

!yolo task=detect mode=predict model=/content/runs/detect/train12/weights/best.pt source=/content/Underwater-Species-Detection-on-BRUVs-4/test/images

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