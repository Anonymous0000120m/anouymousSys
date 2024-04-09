import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from eeg_analysis import load_dataset, preprocess_data, analyze_data

class EEGAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EEG 数据分析")
        self.setGeometry(100, 100, 400, 200)

        self.btn_analyze = QPushButton("分析 EEG 数据", self)
        self.btn_analyze.setGeometry(50, 50, 300, 100)
        self.btn_analyze.clicked.connect(self.analyze_eeg_data)

    def analyze_eeg_data(self):
        # 加载数据集
        eeg_signals, timestamps = load_dataset('dataset.npy')
        if eeg_signals is not None:
            # 预处理数据
            preprocessed_signals = preprocess_data(eeg_signals, timestamps)
            if preprocessed_signals is not None:
                # 分析数据
                results = analyze_data(preprocessed_signals)
                if results is not None:
                    # 显示成功消息框
                    QMessageBox.information(self, "成功", "EEG 数据分析完成！")
                    return
        # 如果出现错误，则显示错误消息框
        QMessageBox.warning(self, "错误", "无法执行 EEG 数据分析！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    eeg_analysis_app = EEGAnalysisApp()
    eeg_analysis_app.show()
    sys.exit(app.exec_())
