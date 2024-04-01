import os  
import re  
from collections import Counter  
from sklearn.feature_extraction import DictVectorizer  
from sklearn.model_selection import train_test_split  
from sklearn.naive_bayes import MultinomialNB  
from sklearn.metrics import classification_report  
  
# Java关键字列表  
java_keywords = set([  
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const',  
    'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float',  
    'for', 'if', 'goto', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native',  
    'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp',  
    'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile',  
    'while', 'true', 'false', 'null'  
])  
  
# 读取文本文件并提取Java关键字  
def extract_java_keywords(text):  
    # 使用正则表达式匹配Java关键字  
    keyword_pattern = r'\b(' + '|'.join(re.escape(kw) for kw in java_keywords) + r')\b'  
    matches = re.findall(keyword_pattern, text, re.IGNORECASE)  
    return matches  
  
# 读取样本文件和标签  
def read_java_samples(directory, label):  
    samples = []  
    for filename in os.listdir(directory):  
        if filename.endswith('.java'):  
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:  
                text = file.read()  
                # 提取Java关键字  
                keywords = extract_java_keywords(text)  
                # 统计每个关键字出现的次数  
                keyword_counts = Counter(keywords)  
                # 将关键字及其计数转换为字典特征  
                features = dict(keyword_counts)  
                samples.append((features, label))  
    return samples  
  
# 假设我们有两个类别的Java代码文件，分别存放在'positive'和'negative'文件夹中  
positive_dir = 'positive'  
negative_dir = 'negative'  
  
# 读取样本  
positive_samples = read_java_samples(positive_dir, 1)  
negative_samples = read_java_samples(negative_dir, 0)  
  
# 合并样本和标签  
samples, labels = zip(*positive_samples + negative_samples)  
  
# 划分数据集  
X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)  
  
# 使用DictVectorizer将字典特征转换为数值向量  
vectorizer = DictVectorizer(sparse=False)  
X_train_features = vectorizer.fit_transform(X_train)  
X_test_features = vectorizer.transform(X_test)  
  
# 初始化分类器  
classifier = MultinomialNB()  
  
# 训练分类器  
classifier.fit(X_train_features, y_train)  
  
# 在测试集上进行预测  
y_pred = classifier.predict(X_test_features)  
  
# 输出分类报告  
print(classification_report(y_test, y_pred))