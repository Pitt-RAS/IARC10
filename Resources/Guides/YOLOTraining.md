# Fine tuning a YOLO model
- Blame Daniel Hufnagle (@fuhd) for errors

# What am I yapping about and why am I yapping about it?
The YOLO (you only look once) model has risen to become one of the best object detection models out there. Having the ability to fine tune it means we can fairly easily get it to successfully detect whatever we want. The fact that we are also just fine tuning means that it is also not very resource intensive to train (as in you can just do it on a free Colab notebook).
# The process
We'll be doing this on a Colab notebook, but really anything with a cuda enabled gpu is fine.
## Install and import dependencies
The one dependency that we actually need to install is ultralytics. This is where we can actually get the YOLO model to train and fine tune.
```python
!pip install ultralytics
```
Now we import the dependencies we need and we'll print whether or not we have access to CUDA. If you are in Colab and it prints false, you need to change the Colab runtime to GPU. After that we mount our google drive (which is where we can upload our dataset).
```python
from ultralytics import YOLO
import torch
from google.colab import drive

print(torch.cuda.is_available())
drive.mount('/content/drive')
```
## Preparations for training
Here we declare our model, the number of epochs we want to train for, and our training device. Before we write any of this code though, we need to create a data.yaml file.
Here is an example of a data.yaml file:
```
train: /content/gdrive/MyDrive/Complete-Blood-Cell-Count-Dataset-Formats/YOLO/Training
val: /content/gdrive/MyDrive/Complete-Blood-Cell-Count-Dataset-Formats/YOLO/Validation
test: /content/gdrive/MyDrive/Complete-Blood-Cell-Count-Dataset-Formats/YOLO/Testing
nc: 3
names:
  0: RBC
  1: WBC
  2: Platelets
```
Essentially, you just have to specify the paths to your training, testing, and validation splits. The number of classes and then their names.
Now that we have that file, let's set some parameters, being the model itself, the number of epochs to train for, and then the device we train on.
```python
model = YOLO('yolov8n.yaml')
epochs = 70
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```
## Training
This it it.
```
model.train(data='data.yaml', epochs=epochs, device=device)
```
After running this (70 epochs should take less than 30 minutes, but yield decent precision), there should be a folder with our model weights. Choose the .pt file in the folder that says best. We can save this locally and then deploy it on the jetson

