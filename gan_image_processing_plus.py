import cv2
import sys
import requests
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
import csv
import os

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

def process_single_image(url, output_csv):
    image_processor = GANImageProcessing(url)
    classification_result = image_processor.classify_image()

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image URL', 'Top Prediction', 'Confidence'])

        top_prediction = classification_result[0]
        writer.writerow([url, top_prediction[1], top_prediction[2]])

def process_batch_images(image_urls_file, output_csv):
    with open(image_urls_file, 'r') as file:
        image_urls = file.readlines()

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image URL', 'Top Prediction', 'Confidence'])

        for url in image_urls:
            url = url.strip()
            image_processor = GANImageProcessing(url)
            classification_result = image_processor.classify_image()
            top_prediction = classification_result[0]
            writer.writerow([url, top_prediction[1], top_prediction[2])

def main(input_param1, input_param2):
    if os.path.isfile(input_param1):  # Check if input_param1 is a file
        process_batch_images(input_param1, input_param2)
    else:
        process_single_image(input_param1, input_param2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the URL of the image or the file containing image URLs and the output CSV file path.")
    else:
        input_param1 = sys.argv[1]
        input_param2 = sys.argv[2]
        main(input_param1, input_param2)
