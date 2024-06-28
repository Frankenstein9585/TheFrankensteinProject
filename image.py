import csv
import itertools

import cv2
import mediapipe as mp

import os

import utils

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils


def process_images(folder_name, csv_name):
    gesture_class_map = {}
    all_landmarks = []
    for idx, folder in enumerate(os.listdir(folder_name)):
        gesture_class_map[idx] = folder
        for filename in os.listdir(os.path.join(folder_name, folder)):
            # Load the image
            image_path = os.path.join(folder, folder_name, filename)  # Replace with the path to your image
            image = cv2.imread(image_path)

            # Crop the image to two-thirds its height to remove unwanted hand
            image = image[:(int((2 / 3) * image.shape[0])), :]

            # Convert the image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and find hands
            results = hands.process(image_rgb)
            # Check if any hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on the image
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    normalized_landmark_list = utils.get_landmark_list(hand_landmarks, image)
                    print(normalized_landmark_list)

                    all_landmarks.append([idx] + normalized_landmark_list)

    # # Display the output image
    #     cv2.imshow('Hand Landmarks', image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    with open(csv_name, 'w', newline='') as file:
        csvwriter = csv.writer(file)
        for landmarks in all_landmarks:
            csvwriter.writerow(landmarks)

    return gesture_class_map


folder_name = 'hagrid_30k'
landmark_csv = 'landmarks.csv'


print(process_images(folder_name, landmark_csv))
