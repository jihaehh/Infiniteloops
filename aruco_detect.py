#!/usr/bin/env python3

import numpy as np
import cv2
import cv2.aruco as aruco
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

# Define the marker IDs and their corresponding letters
id_to_letter = {
    0: 'K',
    1: 'O',
    2: 'R',
    3: 'E',
    4: 'A',
    5: 'M',
    6: 'Y',
    7: 'love'  # Assuming you meant 'heart' for ID 7
}

# dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
# detectorParams = aruco.DetectorParameters()
# detector = cv2.aruco.ArucoDetector(dictionary, detectorParams)

aruco_dict = cv2.aruco.custom_dictionary(0, 5, 1)
aruco_dict.bytesList = np.empty(shape=(8, 4, 4), dtype=np.uint8)

# Define the marker patterns and add them to the dictionary
marker_patterns = [
    [[1, 0, 0, 0, 1],
     [1, 1, 0, 1, 1],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 1, 1]],

    [[0, 1, 1, 1, 0],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [0, 1, 1, 1, 0]],

    [[1, 1, 1, 1, 0],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 0],
     [1, 0, 0, 1, 0],
     [1, 0, 0, 0, 1]],

    [[1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 1, 0],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 1, 1]],

    [[0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1]],

    [[1, 0, 0, 0, 1],
     [1, 1, 0, 1, 1],
     [1, 0, 1, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1]],

    [[1, 0, 0, 0, 1],
     [0, 1, 0, 1, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0]],                           

    [[0, 1, 0, 1, 0],
     [1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1],
     [0, 1, 1, 1, 0],
     [0, 0, 1, 0, 0]]

    # Add other marker patterns here
]

# Add marker patterns to the custom dictionary
for i, pattern in enumerate(marker_patterns):
    aruco_dict.bytesList[i] = aruco.Dictionary_getByteListFromBits(
        np.array(pattern, dtype=np.uint8))


# Initialize the ROS node
rospy.init_node('aruco_marker_detection')
rospy.loginfo('aruco marker detection is running')

# Initialize the video capture from the /camera/image_raw topic
bridge = CvBridge()
image_topic = "/camera/color/image_raw"

def image_callback(msg):
    try:
        # Convert the ROS Image message to a cv2 image
        frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # Detect markers in the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = ""
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            frame, aruco_dict)
        
        # Draw markers and label them with corresponding letters
        detected_letter=''
        if ids is not None:
            for i in range(len(corners)):
                x = int(np.mean(corners[i][0][:, 0]))
                y = int(np.mean(corners[i][0][:, 1]))
                if ids[i][0] in id_to_letter:
                    letter = id_to_letter[ids[i][0]]
                    # print(letter)
                    cv2.putText(frame, 'id = ' + letter, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    
                    detected_letter = letter
            

        # Resize the frame for display
        frame = cv2.resize(frame, None, fx=0.6, fy=0.6)

        # Show the frame
        # cv2.imshow('frame', frame)
        # cv2.waitKey(1)

        # Convert the cv2 image back to a ROS Image message
        image_msg = bridge.cv2_to_imgmsg(frame, encoding="mono8")

        # Publish the image with marker labels
        image_pub.publish(image_msg)
        letter_pub.publish(detected_letter)

    except CvBridgeError as e:
        rospy.loginfo('CvBridge Error: {0}'.format(e))
        print(e)

# Subscribe to the image topic
image_sub = rospy.Subscriber(image_topic, Image, image_callback)

# Create a publisher for the labeled image
labeled_image_topic = "/labeled_image"
detected_letter_topic = "labeled_image/detected_letter"
image_pub = rospy.Publisher(labeled_image_topic, Image, queue_size=10)
letter_pub = rospy.Publisher(detected_letter_topic, String, queue_size=10)
# Spin ROS node
rospy.spin()

# Clean up
# cv2.destroyAllWindows()
