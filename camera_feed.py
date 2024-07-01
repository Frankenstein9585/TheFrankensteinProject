# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
#
#
# # STEP 2: Create an HandLandmarker object.
# base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
# options = vision.HandLandmarkerOptions(base_options=base_options,
#                                        num_hands=2)
# detector = vision.HandLandmarker.create_from_options(options)
#
# # STEP 3: Load the input image.
# image = mp.Image.create_from_file("image.jpg")
#
# # STEP 4: Detect hand landmarks from the input image.
# detection_result = detector.detect(image)
#
# # STEP 5: Process the classification result. In this case, visualize it.
# annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
# cv2_imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
import copy

import cv2
import mediapipe as mp

import utils
from inference_engine import InferenceEngine

# def main():
#     # Initialize MediaPipe Hand model
#     mp_hands = mp.solutions.hands
#     hands = mp_hands.Hands()
#
#     # Initialize webcam
#     cap = cv2.VideoCapture(0)
#
#     while cap.isOpened():
#         # Read frame from webcam
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Convert the image to RGB
#         image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#         # Process the frame
#         results = hands.process(image_rgb)
#
#         # If landmarks are detected, draw them on the image
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 for lm in hand_landmarks.landmark:
#                     # Extract landmark positions
#                     h, w, c = frame.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
#
#         # Display the frame
#         cv2.imshow('Hand Landmarks Detection', frame)
#
#         # Exit if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the webcam and close OpenCV windows
#     cap.release()
#     cv2.destroyAllWindows()

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

            # for i, landmark in enumerate(hand_landmarks.landmark):
            #     x = landmark.x * image.shape[1]
            #     y = landmark.y * image.shape[0]
            #     z = landmark.z * image.shape[1]  # z is normalized similarly to x
            #     # print(f'Landmark {i}: ({x:.2f}, {y:.2f}, {z:.2f})')
            #     print(f'Landmark {i}: {x:.2f} {y:.2f} {z:.2f})')
            normalized_landmark_list = utils.get_landmark_list(hand_landmarks, image)
            gesture_id = inference_engine(normalized_landmark_list)
            image = utils.draw_bounding_box(True, image, bbox)
            image = utils.write_gesture_info(image, bbox, handedness,
                                             gesture_class_names[gesture_id])
    # Display the resulting image
    cv2.imshow('MediaPipe Hand Landmarks', image)

    # Exit loop on 'q' key press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
