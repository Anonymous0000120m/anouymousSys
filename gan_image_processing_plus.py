import cv2
import sys
import requests
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import csv

class GANImageProcessing:
    def __init__(self, url):
        self.url = url
        self.image = self.load_image_from_url()

    def load_image_from_url(self):
        response = requests.get(self.url)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image

    def gray_scale(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return gray_image

    def edge_detection(self):
        edges = cv2.Canny(self.image, 100, 200)
        return edges

    def classify_image(self):
        model = ResNet50(weights='imagenet')
        image = cv2.resize(self.image, (224, 224))
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        preds = model.predict(image)
        decoded_preds = decode_predictions(preds, top=3)[0]
        return decoded_preds

def main(url, output_csv):
    image_processor = GANImageProcessing(url)

    # Classification
    classification_result = image_processor.classify_image()
    print("Classification Result:", classification_result)

    # Save classification result to CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image URL', 'Top Prediction', 'Confidence'])
        writer.writerow([url, classification_result[0][1], classification_result[0][2]])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the URL of the image and the output CSV file path as command line arguments.")
    else:
        url = sys.argv[1]
        output_csv = sys.argv[2]
        main(url, output_csv)
