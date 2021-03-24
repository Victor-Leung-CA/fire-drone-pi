import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

import io
import glob
import scipy.misc
import numpy as np
from six import BytesIO
from PIL import Image, ImageDraw, ImageFont

import tensorflow as tf

import os, sys
# os.environ['PYTHONPATH'] += "./models"

# import sys
# sys.path.append("./models")


from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

#%matplotlib inline


def load_image_into_numpy_array(path):
  
  #img_data = tf.io.gfile.GFile(path, 'rb').read()
  #image = Image.open(BytesIO(img_data))
  #(im_width, im_height, channel) = image.shape
  #return image.astype(np.uint8
    #heavily modified from fritz function
  img_data = tf.io.gfile.GFile(path, 'rb').read()
  image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8) 


#recover our saved model
pipeline_config = './pipeline.config'
#generally you want to put the last ckpt from training in here
model_dir = 'ckpt 0'
print(os.getcwd())
configs = config_util.get_configs_from_pipeline_file(pipeline_config)
model_config = configs['model']
detection_model = model_builder.build(
      model_config=model_config, is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(
      model=detection_model)
ckpt.restore(os.path.join('ckpt-0'))


def get_model_detection_function(model):
  """Get a tf.function for detection."""

  @tf.function
  def detect_fn(image):
    """Detect objects in image."""

    image, shapes = model.preprocess(image)
    prediction_dict = model.predict(image, shapes)
    detections = model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])

  return detect_fn

detect_fn = get_model_detection_function(detection_model)


#map labels for inference decoding
# label_map_path = configs['eval_input_config'].label_map_path
label_map_path='/home/pi/tensorflow1/models/Smoke_label_map.pbtxt'
label_map = label_map_util.load_labelmap(label_map_path)
categories = label_map_util.convert_label_map_to_categories(
    label_map,
    max_num_classes=label_map_util.get_max_label_map_index(label_map),
    use_display_name=True)
category_index = label_map_util.create_category_index(categories)
label_map_dict = label_map_util.get_label_map_dict(label_map, use_display_name=True)

#test image script
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 00:53:43 2021

@author: sarah
"""

#run detector on test image
#takes longer on the first run and then runs at normal speed.
#CAMERA CODE HERE

#test image code, commented out
# test_image_path='/home/pi/tensorflow1/models/FireDroneDet/Photos/smoke1.png'
# image_np = load_image_into_numpy_array(test_image_path)

#CAMERA CODE
import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
# Define the codec and create VideoWriter object
img_counter = 0

img_name = "opencv_frame_{}.png".format(img_counter)
out = cv2.imwrite(img_name, frame)

#camera code modified from fritz tutorial
while(True):
    
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    
    elif k%256 == 32:
        # SPACE pressed, OR MODIFY TO RUN EVERY 5 MINUTES
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        
    ret,image_np = cam.read()
    image_np = load_image_into_numpy_array(image_np)

    input_tensor = tf.convert_to_tensor(
    np.expand_dims(image_np, 0), dtype=tf.float32)
    
    detections, predictions_dict, shapes = detect_fn(input_tensor)

    input_tensor = tf.convert_to_tensor(
        np.expand_dims(image_np, 0), dtype=tf.float32)
    detections, predictions_dict, shapes = detect_fn(input_tensor)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
          image_np_with_detections,
          detections['detection_boxes'][0].numpy(),
          (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
          detections['detection_scores'][0].numpy(),
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=200,
          min_score_thresh=.5,
          agnostic_mode=False,
    )

#only saves output image if there is a detection
if np.any(detections['detection_scores'][0].numpy() >= 0.5):
    plt.figure(figsize=(12,16))
    plt.axis('off')
    plt.imshow(image_np_with_detections)
    plt.show()
    fileName = r'/home/pi/Desktop/detoutput.png'
    plt.savefig(fileName,format='png')   # save the figure to file
    print('SMOKE DETECTED')
    
#ATTEMPT TO INCREMENT FILE NAMES
#     fileNameTemplate = r'/home/pi/Desktop/detoutput{0:02d}.png'
#     rootdir = '/home/pi/Desktop/'
#     
#     for subdir,dirs,files in os.walk(rootdir):
#         for count, file in enumerate(files):
#             # Generate a plot in `pl`
#             plt.savefig(fileNameTemplate.format(count), format='png')
    
      