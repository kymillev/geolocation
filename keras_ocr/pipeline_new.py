# pylint: disable=too-few-public-methods
import numpy as np
import time
import tensorflow as tf

from . import detection, tools
from . import recognition_new as recognition

def parse_image(filename,img_shape=None):

    image = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image)
    image = tf.image.convert_image_dtype(image, tf.float32)
    if img_shape is not None:
        image = tf.image.resize(image, img_shape)
    return image



class Pipeline:
    """A wrapper for a combination of detector and recognizer.

    Args:
        detector: The detector to use
        recognizer: The recognizer to use
        scale: The scale factor to apply to input images
        max_size: The maximum single-side dimension of images for
            inference.
    """
    def __init__(self, detector=None, recognizer=None, scale=2, max_size=2048):
        if detector is None:
            detector = detection.Detector()
        if recognizer is None:
            recognizer = recognition.Recognizer()
        self.scale = scale
        self.detector = detector
        self.recognizer = recognizer
        self.max_size = max_size


    def recognize(self, images, detection_kwargs=None, recognition_kwargs=None,verbose=0):
        """Run the pipeline on one or multiples images.

        Args:
            images: The images to parse (can be a list of actual images or a list of filepaths)
            detection_kwargs: Arguments to pass to the detector call
            recognition_kwargs: Arguments to pass to the recognizer call

        Returns:
            A list of lists of (text, box) tuples.
        """
        t1 = time.time()
        # Make sure we have an image array to start with.
        if not isinstance(images, np.ndarray):
            images = [tools.read(image) for image in images]
        # This turns images into (image, scale) tuples temporarily
        images = [
            tools.resize_image(image, max_scale=self.scale, max_size=self.max_size)
            for image in images
        ]
        max_height, max_width = np.array([image.shape[:2] for image, scale in images]).max(axis=0)
        scales = [scale for _, scale in images]
        images = np.array(
            [tools.pad(image, width=max_width, height=max_height) for image, _ in images])
        if detection_kwargs is None:
            detection_kwargs = {}
        if recognition_kwargs is None:
            recognition_kwargs = {}
        if verbose:
            print('Image preprocessing pipeline:',round(time.time()-t1,3),'s')
        t1 = time.time()
        box_groups = self.detector.detect(images=images, **detection_kwargs)
        if verbose:
            print('Detector time:',round(time.time()-t1,3),'s')
        t1 = time.time()
        prediction_groups = self.recognizer.recognize_from_boxes(images=images,
                                                                 box_groups=box_groups,
                                                                 **recognition_kwargs)
        if verbose:
            print('Recognition time:',round(time.time()-t1,3),'s')
        t1 = time.time()
        box_groups = [
            tools.adjust_boxes(boxes=boxes, boxes_format='boxes', scale=1 /
                               scale) if scale != 1 else boxes
            for boxes, scale in zip(box_groups, scales)
        ]
        if verbose:
            print('Postprocessing time:',round(time.time()-t1,3),'s')
        return [
            list(zip(predictions, boxes))
            for predictions, boxes in zip(prediction_groups, box_groups)
        ]
    
   
    
    def recognize_batch(self, filenames,batch_size=1,pool=None, detection_kwargs=None, recognition_kwargs=None):
        """Run the pipeline on one or multiples images.

        Args:
            images: The images to parse (can be a list of actual images or a list of filepaths)
            detection_kwargs: Arguments to pass to the detector call
            recognition_kwargs: Arguments to pass to the recognizer call

        Returns:
            A list of lists of (text, box) tuples.
        """        
        all_predictions = []
        all_boxes = []
        images = (filenames
                  .map(parse_image)
                  .batch(batch_size))
        
        if detection_kwargs is None:
            detection_kwargs = {}
        if recognition_kwargs is None:
            recognition_kwargs = {}
       
        t1 = time.time()
       
        box_groups = self.detector.detect_batch(images=images,pool=pool, **detection_kwargs)
        
     
        print('Detector time:',round(time.time()-t1,3),'s')
        t1 = time.time()
        prediction_groups = self.recognizer.recognize_from_boxes_batch(images=list(images.as_numpy_iterator()),
                                                                 box_groups=box_groups,
                                                                 **recognition_kwargs)
        print('Recognition time:',round(time.time()-t1,3),'s')
        t1 = time.time()

        print('Postprocessing time:',round(time.time()-t1,3),'s')
        #all_predictions.extend(prediction_groups)
        #all_boxes.extend(box_groups)
       
            
        return [
            list(zip(predictions, boxes))
            for predictions, boxes in zip(prediction_groups, box_groups)
        ]