# analyse .py
import ast
import os

def find_dependencies_in_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    return {node.module for node in ast.walk(tree) if isinstance(node, ast.Import)} | \
           {node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}

def find_dependencies_in_directory(directory):
    dependencies = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                dependencies.update(find_dependencies_in_file(file_path))
    return dependencies

project_directory = '/'  # chemin du projet
dependencies = find_dependencies_in_directory(project_directory)
print(dependencies)

# modif yml
import yaml

def update_yaml_with_dependencies(yaml_file_path, dependencies):
    with open(yaml_file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    
    # les dépendances sont ajoutées dans la section 'dependencies' du yml
    if 'dependencies' not in yaml_content:
        yaml_content['dependencies'] = []
    
    for dependency in dependencies:
        if dependency not in yaml_content['dependencies']:
            yaml_content['dependencies'].append(dependency)
    
    with open(yaml_file_path, 'w') as file:
        yaml.safe_dump(yaml_content, file)

yaml_file_path = 'environment.yml'  # chemin du fichier yml
update_yaml_with_dependencies(yaml_file_path, dependencies)
