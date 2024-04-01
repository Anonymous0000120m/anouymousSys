import mysql.connector  
from jinja2 import Environment, FileSystemLoader  
import os  
  
# 数据库连接参数  
db_config = {  
    'host': 'your_host',  
    'user': 'your_user',  
    'password': 'your_password',  
    'database': 'your_database'  
}  
  
# 生成的 Java 文件的参数  
java_config = {  
    'base_package_name': 'com.example.myapp',  # 基础包名  
    'output_path': 'generated_java_classes',   # 输出路径  
    'module_name': 'MyModule'                   # 模块名（可选，用于文件夹结构）  
}  
  
# 连接到数据库  
connection = mysql.connector.connect(**db_config)  
cursor = connection.cursor()  
  
# 查询数据库中的表  
query = "SHOW TABLES"  
cursor.execute(query)  
tables = cursor.fetchall()  
  
# 创建 Jinja2 环境  
env = Environment(loader=FileSystemLoader('templates'))  
  
# 遍历每个表并生成对应的 Java 类文件  
for (table_name,) in tables:  
    # 查询表的字段信息  
    query = f"DESCRIBE {table_name}"  
    cursor.execute(query)  
    fields = cursor.fetchall()  
  
    # 提取类名（可以根据需要转换表名为类名）  
    class_name = table_name.capitalize()  
  
    # 创建包和模块的目录结构  
    package_name = f"{java_config['base_package_name']}.{java_config['module_name']}.{table_name.lower()}"  
    package_path = os.path.join(java_config['output_path'], *package_name.split('.'))  
    os.makedirs(package_path, exist_ok=True)  
  
    # 渲染模板  
    template = env.get_template('java_class_template.jinja2')  
    rendered_code = template.render(class_name=class_name, package_name=package_name, fields=fields)  
  
    # 写入 Java 文件  
    file_path = os.path.join(package_path, f"{class_name}.java")  
    with open(file_path, 'w') as f:  
        f.write(rendered_code)  
  
# 关闭数据库连接  
cursor.close()  
connection.close()