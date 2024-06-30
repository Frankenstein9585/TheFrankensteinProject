import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


class InferenceEngine(object):
    def __init__(self, model_path='models/best_model.h5'):
        self.model = load_model(model_path)

    def __call__(self, landmark_list):
        input_data = np.array([landmark_list], dtype=np.float32)

        result = self.model.predict(input_data)

        result_index = np.argmax(np.squeeze(result))

        return result_index

