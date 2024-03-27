import os  
from datetime import datetime  
  
# 关键字文件路径  
keywords_file = 'keywords.txt'  
# 文件扩展名列表文件路径  
extensions_file = 'extensions.txt'  
# 要搜索的目录  
search_directory = '/path/to/search/directory'  
# 日志文件路径  
log_file = 'search_log.txt'  
  
# 读取关键字文件  
with open(keywords_file, 'r', encoding='utf-8') as f:  
    keywords = [line.strip() for line in f.readlines()]  
  
# 读取文件扩展名列表  
with open(extensions_file, 'r', encoding='utf-8') as f:  
    extensions = [line.strip().lower() for line in f.readlines()]  
  
# 搜索文件并写入日志  
with open(log_file, 'w', encoding='utf-8') as log:  
    for root, dirs, files in os.walk(search_directory):  
        for file in files:  
            # 检查文件扩展名是否在列表中  
            if os.path.splitext(file)[1][1:].lower() in extensions:  
                file_path = os.path.join(root, file)  
                try:  
                    # 使用UTF-8编码读取文件内容  
                    with open(file_path, 'r', encoding='utf-8') as f:  
                        content = f.read()  
                        for keyword in keywords:  
                            if keyword in content:  
                                # 获取文件信息  
                                file_size = os.path.getsize(file_path)  
                                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                                # 写入日志  
                                log.write(f"日期: {current_time}\n")  
                                log.write(f"详细路径: {file_path}\n")  
                                log.write(f"大小: {file_size} 字节\n")  
                                log.write(f"包含关键字: {keyword}\n\n")  
                                break  # 如果找到关键字，则不再检查其他关键字  
                except UnicodeDecodeError:  
                    # 如果文件不是UTF-8编码，可以记录或跳过  
                    log.write(f"无法读取文件（可能不是UTF-8编码）: {file_path}\n\n")  
  
print("搜索完成，结果已写入日志文件。")