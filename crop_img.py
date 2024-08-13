import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to find hands
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Calculate the bounding box coordinates
            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * image.shape[1]) - 15
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * image.shape[1]) + 15
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * image.shape[0]) - 15
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * image.shape[0]) + 15
            print(x_max - x_min)
            print(y_max - y_min)

            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(image.shape[1], x_max)
            y_max = min(image.shape[0], y_max)

            # Draw the bounding box on the original image
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Crop the ROI containing the hand
            cropped_image = image[y_min:y_max, x_min:x_max]
            resized_image = cv2.resize(cropped_image, (224, 224))

            # Convert the resized image to an array
            processed_image = img_to_array(resized_image)

            # Display the original image with the bounding box
            cv2.imshow("Hand with Bounding Box", image)
            cv2.imshow('Resized Image', resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            return processed_image
    else:
        print("No hand detected")
        return None  # If no hand is detected


# Example usage
processed_image = preprocess_image('0d952f23-f65c-4d06-b928-85c7211fd4b8.jpg')