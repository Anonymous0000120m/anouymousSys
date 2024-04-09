import os
import shutil
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
import librosa
import numpy as np

def extract_audio_features(file_path):
    # 使用 librosa 库加载音频文件并提取特征
    audio_data, _ = librosa.load(file_path, sr=None)
    # 提取音频特征，这里以音频长度作为示例特征
    features = np.array([len(audio_data)])
    return features

def search_mp3_files(directory):
    mp3_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))
    return mp3_files

def cluster_mp3_files(mp3_files, tags_file, output_directory):
    # 读取标签文件，将英文和中文标签分开
    english_tags = []
    chinese_tags = []
    with open(tags_file, 'r', encoding='utf-8') as f:
        for line in f:
            tag_en, tag_cn = line.strip().split(',')
            english_tags.append(tag_en)
            chinese_tags.append(tag_cn)

    # 提取音频特征
    audio_features = []
    for mp3_file in mp3_files:
        audio_features.append(extract_audio_features(mp3_file))

    # 使用 TF-IDF 向量化特征
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(english_tags)

    # 使用 KMeans 聚类算法进行无监督学习
    kmeans = KMeans(n_clusters=len(english_tags))
    pipeline = make_pipeline(Normalizer(), kmeans)
    pipeline.fit(X)

    # 将 MP3 文件按照聚类结果保存到不同的文件夹中
    for i, label in enumerate(kmeans.labels_):
        tag_folder = os.path.join(output_directory, chinese_tags[label])
        if not os.path.exists(tag_folder):
            os.makedirs(tag_folder)
        shutil.copy(mp3_files[i], tag_folder)

def main():
    # 指定要搜索的目录、标签文件和输出目录
    search_directory = 'your_search_directory'
    tags_file = 'your_tags_file.txt'
    output_directory = 'output'

    # 搜索 MP3 文件
    mp3_files = search_mp3_files(search_directory)

    # 对 MP3 文件进行聚类分类
    cluster_mp3_files(mp3_files, tags_file, output_directory)

if __name__ == "__main__":
    main()
