import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
import cv2
import tensorflow as tf

class ImageRecognizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Recognizer")

        self.btnLoadImage = QPushButton("Load Image")
        self.btnLoadImage.clicked.connect(self.loadImage)

        self.labelImage = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.btnLoadImage)
        layout.addWidget(self.labelImage)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.png *.bmp)")
        if filePath:
            image = cv2.imread(filePath)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
            self.labelImage.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QtGui.QImage.Format_RGB888)))

def main():
    app = QApplication(sys.argv)
    mainWindow = ImageRecognizer()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
