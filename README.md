# Infiniteloops

## project summary
This Python code utilizes OpenCV and the ArUco library to detect markers in real-time through a webcam feed. It displays the corresponding letters associated with the detected markers on the webcam screen. The program is designed with the theme of "Korea, and it visually represents content related to a patriotic girl.

The key components of the program include:

1. **Mapping of Markers and Letters:**
   - Utilizes the `id_to_letter` dictionary to map marker identifiers to their corresponding letters.

2. **Initialization of ArUco Dictionary:**
   - Uses the `cv2.aruco.custom_dictionary` function to initialize a custom ArUco dictionary.
   - Defines marker patterns, representing characters such as '한' and '국', and adds them to the dictionary.

3. **Definition and Addition of Marker Patterns:**
   - The `marker_patterns` list defines patterns that visually represent characters like "Korea"
   - Each pattern is added to the ArUco dictionary, allowing for the detection of these characters.

4. **Video Capture and Processing Loop:**
   - Captures real-time video from the webcam and uses the `aruco.detectMarkers` function to identify markers.
   - Extracts the corresponding letters for detected markers and displays them on the webcam screen.

5. **Exit Condition:**
   - The program exits when the user presses the 'q' key.

This example visually represents the theme of a patriotic girl through real-time marker detection, where markers with the characters 'Korea' are identified and displayed on the webcam feed.

## A video about our project
> https://youtu.be/LO_4a9Jqg3w
