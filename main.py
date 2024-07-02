import time

import cv2
import mediapipe as mp

from test import gesture_to_action
import utils
from inference_engine import InferenceEngine

gesture_class_names = utils.get_gesture_class_names('class_names.csv')
inference_engine = InferenceEngine()

mp_hands = mp.solutions.hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)


def execute_action(label):
    if label in gesture_to_action:
        gesture_to_action[label]()


while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a more natural look
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB format for MediaPipe processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run MediaPipe hands detection
    results = mp_hands.process(rgb_image)

    # Draw hand landmarks if a hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            bbox = utils.calculate_bounding_box(image, hand_landmarks)
            normalized_landmark_list = utils.get_landmark_list(hand_landmarks, image)
            gesture_id = inference_engine(normalized_landmark_list)
            label = gesture_class_names[gesture_id]
            image = utils.draw_bounding_box(True, image, bbox)
            image = utils.write_gesture_info(image, bbox, handedness,
                                             label)
    # Display the resulting image
    cv2.imshow('MediaPipe Hand Landmarks', image)

    # Exit loop on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
