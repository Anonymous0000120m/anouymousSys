import os  
import re  
import jinja2  
  
def read_sql_to_java_types(mapping_file):  
    type_mapping = {}  
    with open(mapping_file, 'r') as file:  
        for line in file:  
            sql_type, java_type = line.strip().split(',')  
            type_mapping[sql_type.upper()] = java_type.strip()  
    return type_mapping  
  
def parse_sql_for_tables(sql_file_path):  
    tables = {}  
    with open(sql_file_path, 'r') as file:  
        sql_content = file.read()  
        # 假设表定义以 CREATE TABLE 开头，且每个表的定义是独立的  
        table_pattern = re.compile(r"CREATE TABLE (\w+) \((.*?)\);", re.DOTALL | re.IGNORECASE)  
        table_matches = table_pattern.findall(sql_content)  
        for table_name, fields in table_matches:  
            fields = re.findall(r"(\w+)\s+(\w+)", fields)  
            tables[table_name] = {field[0]: field[1] for field in fields}  
    return tables  
  
def generate_entity_classes(sql_file_path, template_dir, type_mapping, package_name, output_dir):  
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)  
    tables = parse_sql_for_tables(sql_file_path)  
  
    for table_name, fields in tables.items():  
        class_name = table_name.title().replace('_', '')  
        template = template_env.get_template('Entity.jinja2')  
        fields_with_types = [(field, type_mapping.get(fields[field].upper(), 'java.lang.Object')) for field in fields]  
        rendered = template.render(class_name=class_name, fields=fields_with_types, package_name=package_name)  
        output_file_path = os.path.join(output_dir, f'{package_name.replace(".", os.path.sep)}{os.path.sep}{class_name}.java')  
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  
        with open(output_file_path, 'w') as file:  
            file.write(rendered)  
        print(f'Generated class for table {table_name}: {output_file_path}')  
  
# 示例用法  
sql_file_path = 'path/to/your/sqlfile.sql'  
template_dir = 'path/to/your/templates'  
type_mapping_file = 'path/to/your/sql_to_java_types.txt'  
package_name = 'com.example.database'  
output_dir = 'path/to/output/directory'  
  
# 读取 SQL 类型到 Java 类型的映射  
sql_to_java_types_dict = read_sql_to_java_types(type_mapping_file)  
  
# 生成实体类  
generate_entity_classes(sql_file_path, template_dir, sql_to_java_types_dict, package_name, output_dir)