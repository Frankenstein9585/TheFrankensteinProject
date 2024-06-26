import itertools

import pandas as pd
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green


def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image


def normalize_landmarks(landmarks):
    base_x = landmarks[0].x
    base_y = landmarks[0].y
    base_z = landmarks[0].z
    normalized_landmarks = []
    for lm in landmarks:
        normalized_landmarks.append([lm.x - base_x, lm.y - base_y, lm.z - base_z])
    return normalized_landmarks


def normalize_landmarks_by_image_dimensions(hand_landmarks, image):
    for i, landmark in enumerate(hand_landmarks.landmark):
        landmark.x = landmark.x * image.shape[1]
        landmark.y = landmark.y * image.shape[0]
        landmark.z = landmark.z * image.shape[1]
    return hand_landmarks.landmark


def get_landmark_list(hand_landmarks, image):
    new_landmarks = normalize_landmarks_by_image_dimensions(hand_landmarks, image)
    normalized_landmarks = normalize_landmarks(new_landmarks)
    landmark_list = list(itertools.chain.from_iterable(normalized_landmarks))
    max_value = max(map(abs, landmark_list))
    normalized_landmark_list = list(map(lambda n: n / max_value, landmark_list))
    return normalized_landmark_list


def calculate_bounding_box(image, hand_landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(hand_landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def draw_bounding_box(use_bbox, image, bbox):
    if use_bbox:
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                      (0, 0, 0), 1)

        return image


def write_gesture_info(image, bbox, handedness, gesture_info):
    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[1] - 22),
                  (0, 0, 0), -1)
    gesture_text = handedness.classification[0].label[0:]
    if gesture_info != '':
        gesture_text = gesture_text + ':' + gesture_info
    cv2.putText(image, gesture_text, (bbox[0] + 5, bbox[1] - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    return image


def get_gesture_class_names(path_to_csv):
    df = pd.read_csv(path_to_csv)
    gesture_class_names = list(df['Class Name'])
    return gesture_class_names


def increase_exposure(frame, alpha=1.0, beta=50):
    new_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    return new_frame
