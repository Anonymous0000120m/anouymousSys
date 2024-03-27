import os  
import shutil  
from datetime import datetime  
from pathlib import Path  
  
# 替换规则文件路径  
replacements_file = 'replacements.txt'  
# 要搜索的目录  
search_directory = '/path/to/search/directory'  
# 日志文件路径  
log_file = 'replacement_log.txt'  
  
# 读取替换规则  
with open(replacements_file, 'r', encoding='utf-8') as f:  
    replacements = [line.strip().split(' -> ') for line in f.readlines() if line.strip()]  
  
# 将替换规则转换为字典，以提高查找效率  
replacement_dict = {old: new for old, new in replacements}  
  
# 遍历目录并应用替换规则  
with open(log_file, 'w', encoding='utf-8') as log:  
    for root, dirs, files in os.walk(search_directory):  
        for file in files:  
            file_path = os.path.join(root, file)  
            relative_path = os.path.relpath(file_path, search_directory)  
  
            # 检查是否需要替换  
            for old, new in replacement_dict.items():  
                if old in relative_path:  
                    new_relative_path = relative_path.replace(old, new)  
                    new_dir = os.path.join(search_directory, os.path.dirname(new_relative_path))  
                    new_file_path = os.path.join(new_dir, os.path.basename(new_relative_path))  
  
                    # 创建新目录（如果不存在）  
                    os.makedirs(new_dir, exist_ok=True)  
  
                    # 复制文件到新路径并重命名（如果新文件不存在）  
                    if not os.path.exists(new_file_path):  
                        shutil.copy2(file_path, new_file_path)  
  
                        # 获取文件信息并写入日志  
                        file_size = os.path.getsize(new_file_path)  
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                        log.write(f"日期: {current_time}\n")  
                        log.write(f"大小: {file_size} 字节\n")  
                        log.write(f"原路径: {file_path}\n")  
                        log.write(f"新路径: {new_file_path}\n\n")  
  
print("文件替换完成，结果已写入日志文件。")