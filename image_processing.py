import cv2  
import requests  
import numpy as np  
  
class ImageProcessing:  
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
  
    def rgb_processing(self):  
        # 示例：将图像转换为HSV色彩空间，并增强饱和度  
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)  
        hsv_image = np.array(hsv_image, dtype=np.float32)  
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.5, 0, 255)  # 增强饱和度  
        hsv_image = np.array(hsv_image, dtype=np.uint8)  
        processed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)  
        return processed_image  
  
    def edge_detection(self):  
        edges = cv2.Canny(self.image, 100, 200)  
        return edges  
  
# 替换为您的图像URL  
url = "YOUR_IMAGE_URL_HERE"  
image_processor = ImageProcessing(url)  
  
# 灰度处理  
gray_image = image_processor.gray_scale()  
cv2.imshow('Gray Image', gray_image)  
cv2.waitKey(0)  
  
# RGB处理  
processed_image = image_processor.rgb_processing()  
cv2.imshow('Processed Image', processed_image)  
cv2.waitKey(0)  
  
# 边缘检测  
edges = image_processor.edge_detection()  
cv2.imshow('Edge Detection', edges)  
cv2.waitKey(0)  
  
cv2.destroyAllWindows()