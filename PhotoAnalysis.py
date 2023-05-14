#Note: The photo analysis program must be used in google colabs 

from string import whitespace
from google.colab import drive
drive.mount('/content/gdrive')

# import dependencies
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import cv2
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from IPython.display import display, Javascript, Image
from google.colab.output import eval_js
from base64 import b64decode, b64encode
import base64
import PIL
import io
import html
import time
from PIL import Image
from google.colab.patches import cv2_imshow


#Get Python and OpenCV Version
print('OpenCV-Python Lib Version:', cv2.__version__)
print('Python Version:',sys.version)

#global variables

#folders (str format)
METAL = "Metal"
RED = "Red"
whitespace = "White"

#imaging options
RGB = "RGB"
GRAYSCALE = "GRAYSCALE"
BINARY = "BINARY"


def main():
    # Get the image
    #img = getImgObject(METAL, "Metal_6.jpg", GRAYSCALE)
    img = getImgObject(RED, "6_some_holes_covered.jpg", GRAYSCALE)
    if img is None:
        print("Image not loaded")
        return

    # Set up the SimpleBlobDetector parameters
    blob_params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    blob_params.minThreshold = 10
    blob_params.maxThreshold = 200

    # Filter by Area.
    blob_params.filterByArea = True
    blob_params.minArea = 100

    # Filter by Circularity
    blob_params.filterByCircularity = True
    blob_params.minCircularity = 0.1

    # Filter by Convexity
    blob_params.filterByConvexity = True
    blob_params.minConvexity = 0.87

    # Filter by Inertia
    blob_params.filterByInertia = True
    blob_params.minInertiaRatio = 0.1

    # Create a blob detector with the parameters
    blob_detector = cv2.SimpleBlobDetector_create(blob_params)

    # Detect blobs
    keypoints = blob_detector.detect(img)

    # Prepare a color version of the image for visualization
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Apply adaptive mean thresholding
    img_bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and hierarchy
    for i, cnt in enumerate(contours):
        # We need at least 5 points to fit an ellipse
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            # Get the size of the ellipse
            (center_x, center_y), (MA, ma), angle = ellipse
            # Calculate the ratio of the major axis to the minor axis
            ratio = ma / MA if MA > 0 else 0
            # If the size of the ellipse and the ratio are within the range, draw it
            if 20 <= MA <= 100 and 20 <= ma <= 100 and 1 <= ratio <= 3:
                # Check if it has a corresponding blob (circle)
                for kp in keypoints:
                    x_ellipse, y_ellipse = int(center_x), int(center_y)
                    x_blob, y_blob = int(kp.pt[0]), int(kp.pt[1])
                    distance = np.sqrt((x_ellipse - x_blob) ** 2 + (y_ellipse - y_blob) ** 2)
                    if distance <= 10:  # Adjust the distance threshold as needed
                        # Draw the overlapping ellipse in red
                        cv2.ellipse(img_color, ellipse, (0, 0, 255), 2)
                        # Draw a circle around the keypoint (blob) in green
                        cv2.circle(img_color, (x_blob, y_blob), int(kp.size / 2), (0, 255, 0), 2)
                        # Add the word "circle" on the image where the green circle and red ellipse overlap
                        cv2.putText(img_color, "circle", (x_blob, y_blob), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the original image and the result
    printToScreen(img, True)
    printToScreen(img_color, False)

def js_to_image(js_reply):
  """
  Params:
          js_reply: JavaScript object containing image from webcam
  Returns:
          img: OpenCV BGR image
  """
  # decode base64 image
  image_bytes = base64.b64decode(js_reply.split(',')[1])
  # convert bytes to numpy array
  jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
  # decode numpy array into OpenCV BGR image
  img = cv2.imdecode(jpg_as_np, flags=1)

  return img

def getImgObject(folder, file, imaging):
  string = '/content/gdrive/My Drive/Toyota Challenge/Training Images/' + folder + "/" + file
  
  print(string)

  if(imaging=="RGB"):
    img = cv2.imread(string, cv2.IMREAD_UNCHANGED)
  elif(imaging=="GRAYSCALE"):
    img = cv2.imread(string, cv2.IMREAD_GRAYSCALE)
  else:
    gray = cv2.imread(string, cv2.IMREAD_GRAYSCALE)
    # binary threshholding -> convert grayscale -> binary img
    ret, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

  return img

def printToScreen(img, grayQ):
  plt.figure(figsize=(10,10))
  if (grayQ):
    plt.imshow(img, cmap="gray")
  else:
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  plt.title('image')
  plt.show()

# JavaScript to properly create our live video stream using our webcam as input
def video_stream():
  js = Javascript('''
    var video;
    var div = null;
    var stream;
    var captureCanvas;
    var imgElement;
    var labelElement;
    
    var pendingResolve = null;
    var shutdown = false;
    
    function removeDom() {
       stream.getVideoTracks()[0].stop();
       video.remove();
       div.remove();
       video = null;
       div = null;
       stream = null;
       imgElement = null;
       captureCanvas = null;
       labelElement = null;
    }
    
    function onAnimationFrame() {
      if (!shutdown) {
        window.requestAnimationFrame(onAnimationFrame);
      }
      if (pendingResolve) {
        var result = "";
        if (!shutdown) {
          captureCanvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
          result = captureCanvas.toDataURL('image/jpeg', 0.8)
        }
        var lp = pendingResolve;
        pendingResolve = null;
        lp(result);
      }
    }
    
    async function createDom() {
      if (div !== null) {
        return stream;
      }

      div = document.createElement('div');
      div.style.border = '2px solid black';
      div.style.padding = '3px';
      div.style.width = '100%';
      div.style.maxWidth = '600px';
      document.body.appendChild(div);
      
      const modelOut = document.createElement('div');
      modelOut.innerHTML = "<span>Status:</span>";
      labelElement = document.createElement('span');
      labelElement.innerText = 'No data';
      labelElement.style.fontWeight = 'bold';
      modelOut.appendChild(labelElement);
      div.appendChild(modelOut);
           
      video = document.createElement('video');
      video.style.display = 'block';
      video.width = div.clientWidth - 6;
      video.setAttribute('playsinline', '');
      video.onclick = () => { shutdown = true; };
      stream = await navigator.mediaDevices.getUserMedia(
          {video: { facingMode: "environment"}});
      div.appendChild(video);

      imgElement = document.createElement('img');
      imgElement.style.position = 'absolute';
      imgElement.style.zIndex = 1;
      imgElement.onclick = () => { shutdown = true; };
      div.appendChild(imgElement);
      
      const instruction = document.createElement('div');
      instruction.innerHTML = 
          '<span style="color: red; font-weight: bold;">' +
          'When finished, click here or on the video to stop this demo</span>';
      div.appendChild(instruction);
      instruction.onclick = () => { shutdown = true; };
      
      video.srcObject = stream;
      await video.play();

      captureCanvas = document.createElement('canvas');
      captureCanvas.width = 640; //video.videoWidth;
      captureCanvas.height = 480; //video.videoHeight;
      window.requestAnimationFrame(onAnimationFrame);
      
      return stream;
    }
    async function stream_frame(label, imgData) {
      if (shutdown) {
        removeDom();
        shutdown = false;
        return '';
      }

      var preCreate = Date.now();
      stream = await createDom();
      
      var preShow = Date.now();
      if (label != "") {
        labelElement.innerHTML = label;
      }
            
      if (imgData != "") {
        var videoRect = video.getClientRects()[0];
        imgElement.style.top = videoRect.top + "px";
        imgElement.style.left = videoRect.left + "px";
        imgElement.style.width = videoRect.width + "px";
        imgElement.style.height = videoRect.height + "px";
        imgElement.src = imgData;
      }
      
      var preCapture = Date.now();
      var result = await new Promise(function(resolve, reject) {
        pendingResolve = resolve;
      });
      shutdown = false;
      
      return {'create': preShow - preCreate, 
              'show': preCapture - preShow, 
              'capture': Date.now() - preCapture,
              'img': result};
    }
    ''')

  display(js)
  
def bbox_to_bytes(bbox_array):
    """
    Converts bounding box into bytes for overlay on video stream.
    """
    # convert array into PIL image
    bbox_PIL = PIL.Image.fromarray(bbox_array, 'RGBA')
    iobuf = io.BytesIO()
    # format bbox into png for return
    bbox_PIL.save(iobuf, format='png')
    # format return string
    bbox_bytes = 'data:image/png;base64,{}'.format((str(b64encode(iobuf.getvalue()), 'utf-8')))

    return bbox_bytes

def video_frame(label, bbox):
  data = eval_js('stream_frame("{}", "{}")'.format(label, bbox))
  return data

def process_frame(img):
    # Set up the SimpleBlobDetector parameters
    blob_params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    blob_params.minThreshold = 10
    blob_params.maxThreshold = 200

    # Filter by Area.
    blob_params.filterByArea = True
    blob_params.minArea = 100

    # Filter by Circularity
    blob_params.filterByCircularity = True
    blob_params.minCircularity = 0.1

    # Filter by Convexity
    blob_params.filterByConvexity = True
    blob_params.minConvexity = 0.87

    # Filter by Inertia
    blob_params.filterByInertia = True
    blob_params.minInertiaRatio = 0.1

    # Create a blob detector with the parameters
    blob_detector = cv2.SimpleBlobDetector_create(blob_params)

    # Detect blobs
    keypoints = blob_detector.detect(img)

    # Prepare a color version of the image for visualization
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Apply adaptive mean thresholding
    img_bin = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and hierarchy
    for i, cnt in enumerate(contours):
        # We need at least 5 points to fit an ellipse
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            # Get the size of the ellipse
            (center_x, center_y), (MA, ma), angle = ellipse
            # Calculate the ratio of the major axis to the minor axis
            ratio = ma / MA if MA > 0 else 0
            # If the size of the ellipse and the ratio are within the range, draw it
            if 20 <= MA <= 100 and 20 <= ma <= 100 and 1 <= ratio <= 3:
                # Check if it has a corresponding blob (circle)
                for kp in keypoints:
                    x_ellipse, y_ellipse = int(center_x), int(center_y)
                    x_blob, y_blob = int(kp.pt[0]), int(kp.pt[1])
                    distance = np.sqrt((x_ellipse - x_blob) ** 2 + (y_ellipse - y_blob) ** 2)
                    if distance <= 10:  # Adjust the distance threshold as needed
                        # Draw the overlapping ellipse in red
                        cv2.ellipse(img_color, ellipse, (0, 0, 255), 2)
                        # Draw a circle around the keypoint (blob) in green
                        cv2.circle(img_color, (x_blob, y_blob), int(kp.size / 2), (0, 255, 0), 2)
                        # Add the word "circle" on the image where the green circle and red ellipse overlap
                        cv2.putText(img_color, "circle", (x_blob, y_blob), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return img_color




# start streaming video from webcam
video_stream()
# label for video
label_html = 'Capturing...'
# initialze bounding box to empty
bbox = ''
count = 0 

# initialize the Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

# Now, use this function in your video stream processing loop:

while True:
    js_reply = video_frame(label_html, bbox)
    if not js_reply:
        break

    # convert JS response to OpenCV Image
    img = js_to_image(js_reply["img"])

    # create transparent overlay for bounding box
    bbox_array = np.zeros([480,640,4], dtype=np.uint8)

    # grayscale image for blob detection
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # get processed image with blobs and contours
    processed_img = process_frame(gray)
    bbox_array = cv2.cvtColor(processed_img, cv2.COLOR_BGR2BGRA)

    bbox_bytes = bbox_to_bytes(bbox_array)
    bbox = bbox_bytes

    # Display the resulting frame with bounding boxes and detected circles
    cv2_imshow(img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()