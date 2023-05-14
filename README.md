# Toyota RAV-4 Sticker and Hole Automation Algorithm


<p align="center">
  <img width="910" height="476" src="https://github.com/joeymaillette04/ToyotaCV/assets/71158927/2013dad9-ea8d-4242-b627-1b55092d4469">
</p>

#### Development Team: [Camron Sabahi-Pourkashani](https://github.com/csabahi), [Joey Maillette](https://github.com/joeymaillette04), [Shameer Ali](https://github.com/shvhmeer786), [Jeffrey Luo](https://github.com/Jeffbhluo)


## Introduction
This proposal outlines a reliable solution for utilizing automation to detect and inspect holes in engine bays that are covered by stickers. The objective is to develop a program capable of analyzing a live feed of an engine bay during the sticker application process, automatically identifying any holes that are not filled with a specific precision (e.g., 3mm), thus ensuring the quality and precision of the sticker application.

## Solution Overview:
To achieve the desired automation, we propose the following solution components and workflow:

### Live Feed Acquisition: 
Set up a high-resolution camera or a network of cameras to capture a live feed of the engine bay during the sticker application process. The camera(s) should be strategically positioned to provide optimal coverage of the entire engine bay area.

### Image Processing and Analysis:
1. Preprocessing: Apply image preprocessing techniques to enhance the image quality and remove any noise or artifacts that may interfere with subsequent analysis steps. This may involve operations such as noise reduction, image enhancement, and calibration.

2. Hole Detection: Apply computer vision techniques to identify potential hole locations based on the sticker positions. This can involve edge detection, contour analysis, or template matching methods to locate areas with missing stickers, which may indicate the presence of holes.

3. Precision Measurement: Calculate the size of detected holes by measuring their dimensions accurately. This can be accomplished by leveraging image processing techniques, such as morphological operations, edge detection, or shape analysis.

### Hole Inspection and Validation:
1. Thresholding: Set a predetermined precision threshold, such as 3mm, to differentiate between acceptable and unacceptable hole thresholds. Holes exceeding this threshold will be flagged as potential defects.

2. Reporting and Alerting: Generate real-time reports to alert operators about any identified defective holes/sticker coverages that require further inspection or rectification.

### Implementation and Integration:
1. Software Development: Develop a robust software application that integrates the various components mentioned above into a cohesive system.

2. Hardware Integration: Establish a seamless connection between the live feed acquisition system and the software application for real-time data transfer and analysis.

3. Testing and Optimization: Conduct extensive testing to ensure the accuracy, reliability, and speed of the system. Optimize the algorithms and parameters as necessary to achieve the desired performance.

## Built With
In order to develop this computer vision algorithm, we have utilized various python frameworks:

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
* ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
* ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
* ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
* ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)


## Conclusion
By implementing the proposed solution, which combines advanced image processing techniques, object detection, and machine learning algorithms, we can achieve reliable automation for detecting and inspecting holes in engine bays covered by stickers. This solution will enhance quality control processes and ensure the precise application of stickers within the specified tolerances.
