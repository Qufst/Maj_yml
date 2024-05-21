import ast
import os

def find_dependencies_in_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def find_dependencies_in_directory(directory):
    dependencies = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') or file.endswith('.ipynb') or file.endswith('.qmd'):
                file_path = os.path.join(root, file)
                dependencies.update(find_dependencies_in_file(file_path))
    return dependencies

def update_yml_with_dependencies(yml_file, dependencies):
    with open(yml_file, 'r') as file:
        lines = file.readlines()

    with open(yml_file, 'w') as file:
        for line in lines:
            file.write(line)
            if line.strip() == 'dependencies:':
                for dep in sorted(dependencies):
                    file.write(f'  - {dep}\n')

if __name__ == "__main__":
    project_directory = '.'  # Changez ce chemin si nécessaire
    yml_file = 'environment.yml'  # Changez ce chemin si nécessaire
    dependencies = find_dependencies_in_directory(project_directory)
    update_yml_with_dependencies(yml_file, dependencies)
