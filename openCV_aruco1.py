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

]
# Add marker patterns to the custom dictionary
for i, pattern in enumerate(marker_patterns):
    aruco_dict.bytesList[i] = aruco.Dictionary_getByteListFromBits(
        np.array(pattern, dtype=np.uint8))

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict)


 # Draw markers and label them with corresponding letters
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

    # Display the frame
    cv2.imshow('frame', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

