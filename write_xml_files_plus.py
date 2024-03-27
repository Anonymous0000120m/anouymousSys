import os  
import xml.etree.ElementTree as ET  
import logging  
from datetime import datetime  
  
# 设置日志配置  
logging.basicConfig(filename='operation.log', level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s')  
  
def read_xml_files_from_directory(directory):  
    xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]  
    xml_data = []  
    for file in xml_files:  
        file_path = os.path.join(directory, file)  
        try:  
            tree = ET.parse(file_path)  
            root = tree.getroot()  
            # 这里你可以根据需要对XML数据进行处理，例如提取某些元素  
            xml_data.append((file, ET.tostring(root, encoding='utf8').decode('utf8')))  
            logging.info(f"Successfully read XML file: {file_path}")  
        except ET.ParseError as e:  
            logging.error(f"Error parsing XML file: {file_path}, Error: {e}")  
    return xml_data  
  
def write_xml_to_directory(xml_data, directory):  
    if not os.path.exists(directory):  
        os.makedirs(directory)  
    for file_name, xml_content in xml_data:  
        file_path = os.path.join(directory, file_name)  
        try:  
            with open(file_path, 'w', encoding='utf-8') as f:  
                f.write(xml_content)  
            logging.info(f"Successfully wrote XML to file: {file_path}")  
        except IOError as e:  
            logging.error(f"Error writing XML to file: {file_path}, Error: {e}")  
  
# 示例使用  
source_dir = 'path_to_source_directory'  # 替换为你的源XML文件目录  
target_dir = 'path_to_target_directory'  # 替换为你的目标目录，用于写入XML文件  
  
xml_data = read_xml_files_from_directory(source_dir)  
write_xml_to_directory(xml_data, target_dir)