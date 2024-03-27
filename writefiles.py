import os  
import shutil  
import logging  
from datetime import datetime  
  
# 设置日志配置  
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s',  
                    filename='operation_log.log',  
                    filemode='w')  
  
def get_file_size(file_path):  
    """获取文件大小（字节）"""  
    return os.path.getsize(file_path)  
  
def copy_files_with_extension(source_dir, target_dir, extension):  
    """  
    批量复制指定扩展名的文件从源目录到目标目录。  
    """  
    if not os.path.exists(target_dir):  
        os.makedirs(target_dir)  
      
    for filename in os.listdir(source_dir):  
        if filename.endswith(extension):  
            source_file = os.path.join(source_dir, filename)  
            target_file = os.path.join(target_dir, filename)  
            try:  
                # 记录文件信息  
                file_size = get_file_size(source_file)  
                logging.info(f"Copying file: {source_file}, Size: {file_size} bytes")  
                  
                # 复制文件  
                shutil.copy2(source_file, target_file)  
                logging.info(f"File copied to: {target_file}")  
            except shutil.Error as e:  
                logging.error(f"Error copying file {source_file} to {target_file}: {e}")  
            except OSError as e:  
                logging.error(f"Error while accessing the file {source_file}: {e.strerror}")  
            except Exception as e:  
                logging.error(f"Unexpected error occurred while copying {source_file}: {e}")  
  
# 示例使用  
source_directory = 'path_to_source_directory'  # 源目录，包含要复制的文件  
target_directory = 'path_to_target_directory'  # 目标目录，用于存放复制的文件  
file_extension = '.txt'  # 要复制的文件扩展名  
  
# 执行批量复制操作  
copy_files_with_extension(source_directory, target_directory, file_extension)