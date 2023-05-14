#imports
import cv2
import numpy as np

# Set up the SimpleBlobDetector parameters
blob_params = cv2.SimpleBlobDetector_Params()

# Change thresholds
blob_params.minThreshold = 10
blob_params.maxThreshold = 200

# Filter by Area
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

def process_frame(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect blobs
    keypoints = blob_detector.detect(gray)

    # Prepare a color version of the image for visualization
    img_color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Apply adaptive mean thresholding
    img_bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

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
            if 10 <= MA <= 100 and 10 <= ma <= 100 and 1 <= ratio <= 10:
                
                # Check if it has a corresponding blob (circle)
                for kp in keypoints:
                    
                    x_ellipse, y_ellipse = int(center_x), int(center_y)
                    x_blob, y_blob = int(kp.pt[0]), int(kp.pt[1])
                    distance = np.sqrt((x_ellipse - x_blob) ** 2 + (y_ellipse - y_blob) ** 2)
                   
                    if distance <= 20:  # Adjust the distance threshold as needed (depending on distance to holes)
                        
                        # Draw the ellipse in red
                        cv2.ellipse(img_color, ellipse, (0, 0, 255), 2)
                        # Draw circles around the keypoints (blobs) in green
                        cv2.circle(img_color, (x_blob, y_blob), int(kp.size / 2), (0, 255, 0), 2)
                        # Add the word "circle" on the image where the green circle and red ellipse overlap
                        cv2.putText(img_color, "circle", (x_blob, y_blob), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return img_color

# Start capturing frames from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        break

    # Process the frame
    processed_frame = process_frame(frame)

    # Display the processed frame
    cv2.imshow('Processed Frame', processed_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

