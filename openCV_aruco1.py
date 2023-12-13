import numpy as np
import cv2
import cv2.aruco as aruco

# Define the marker IDs and their corresponding letters
id_to_letter = {
    0: 'K',
    1: 'O',
    2: 'R',
    3: 'E',
    4: 'A',
}

aruco_dict = cv2.aruco.custom_dictionary(0, 5, 1)
aruco_dict.bytesList = np.empty(shape=(5, 4, 4), dtype=np.uint8)
