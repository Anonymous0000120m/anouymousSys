import os  
import shutil  
from collections import defaultdict  
  
# 假设文本文件命名规则为 {模块名}.txt  
def extract_module_name_from_file(file_path):  
    # 获取文件名（不含扩展名）作为模块名  
    return os.path.splitext(os.path.basename(file_path))[0]  
  
# 读取文本文件，并假设每行是一个Java实体类的名称  
def read_java_class_names_from_text_file(file_path):  
    with open(file_path, 'r') as file:  
        return file.read().splitlines()  
  
# 将Java实体类文件移动到目标目录  
def move_java_classes_to_target_dir(class_names, output_dir, target_dir):  
    for class_name in class_names:  
        java_file_path = os.path.join(output_dir, f"{class_name}.java")  
        if os.path.exists(java_file_path):  
            module_target_dir = os.path.join(target_dir, module_name)  
            shutil.move(java_file_path, module_target_dir)  
            print(f"Moved {java_file_path} to {module_target_dir}")  
        else:  
            print(f"Java file not found: {java_file_path}")  
  
# 主函数  
def organize_java_classes(text_files_dir, output_dir, target_dir):  
    java_class_classifier = defaultdict(list)  
      
    # 遍历文本文件目录  
    for root, dirs, files in os.walk(text_files_dir):  
        for file in files:  
            if file.endswith('.txt'):  
                file_path = os.path.join(root, file)  
                module_name = extract_module_name_from_file(file_path)  
                class_names = read_java_class_names_from_text_file(file_path)  
                java_class_classifier[module_name].extend(class_names)  
      
    # 移动Java实体类文件到目标目录  
    for module_name, class_names in java_class_classifier.items():  
        move_java_classes_to_target_dir(class_names, output_dir, target_dir)  
  
# 示例用法  
text_files_dir = 'path/to/your/text/files'  # 文本文件所在的目录  
output_dir = 'path/to/output/directory'      # 假设Java实体类文件生成的目录  
target_dir = 'path/to/target/directory'      # 目标目录，用于按模块分类存放Java文件  
  
organize_java_classes(text_files_dir, output_dir, target_dir)