import numpy as np
import onnxruntime as ort


class CustomFeatureExtractor:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.session, self.input_name, self.output_name = self.load_onnx_model(
            model_path
        )

    @staticmethod
    def load_onnx_model(model_path: str):
        session = ort.InferenceSession(model_path)
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        return session, input_name, output_name

    def preprocess_image(self, image):
        img_data = np.array(image).transpose(2, 0, 1).astype(np.float32)
        img_data /= 255.0
        img_data = (img_data - 0.5) / 0.5

        return img_data[np.newaxis, :, :, :]

    def __call__(self, image):
        img_preprocessed = self.preprocess_image(image)
        ort_inputs = {self.input_name: np.array(img_preprocessed)}
        features = self.session.run([self.output_name], ort_inputs)[0]
        return features
