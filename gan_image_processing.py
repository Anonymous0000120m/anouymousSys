import cv2
import sys
import requests
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Reshape, Flatten, Conv2D, Conv2DTranspose
from tensorflow.keras.models import Sequential

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

def build_generator():
    model = Sequential([
        Dense(7*7*256, input_shape=(100,)),
        Reshape((7, 7, 256)),
        Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', activation='relu'),
        Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', activation='relu'),
        Conv2DTranspose(3, (5, 5), strides=(2, 2), padding='same', activation='tanh')
    ])
    return model

def main(url):
    image_processor = GANImageProcessing(url)

    # Generating and processing generated image
    generator = build_generator()
    noise = tf.random.normal([1, 100])
    generated_image = generator(noise, training=False)

    # Gray scale processing
    gray_image = image_processor.gray_scale()
    cv2.imshow('Gray Image', gray_image)
    cv2.waitKey(0)

    # Edge Detection
    edges = image_processor.edge_detection()
    cv2.imshow('Edge Detection', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the URL of the image as a command line argument.")
    else:
        url = sys.argv[1]
        main(url)
