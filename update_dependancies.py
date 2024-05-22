#import ast
#import os
#from tqdm import tqdm
#
#def find_dependencies_in_file(file_path):
#    with open(file_path, 'r') as file:
#        tree = ast.parse(file.read(), filename=file_path)
#    
#    imports = set()
#    for node in ast.walk(tree):
#        if isinstance(node, ast.Import):
#            for alias in node.names:
#                imports.add(alias.name.split('.')[0])
#        elif isinstance(node, ast.ImportFrom):
#            if node.module:
#                imports.add(node.module.split('.')[0])
#    return imports
#
#def find_dependencies_in_directory(directory):
#    dependencies = set()
#    for root, _, files in os.walk(directory):
#        for file in files:
#            if file.endswith('.py') or file.endswith('.ipynb') or file.endswith('.qmd'):
#                file_path = os.path.join(root, file)
#                dependencies.update(find_dependencies_in_file(file_path))
#    return dependencies
#
#def update_yml_with_dependencies(yml_file, dependencies):
#    with open(yml_file, 'r') as file:
#        lines = file.readlines()
#
#    with open(yml_file, 'w') as file:
#        for line in lines:
#            file.write(line)
#            if line.strip() == 'dependencies:':
#                for dep in sorted(dependencies):
#                    file.write(f'  - {dep}\n')
#
#if __name__ == "__main__":
#    project_directory = '.'  # Changez ce chemin si nécessaire
#    yml_file = 'environment.yml'  # Changez ce chemin si nécessaire
#    dependencies = find_dependencies_in_directory(project_directory)
#    update_yml_with_dependencies(yml_file, dependencies)

#%%
from tqdm import tqdm
import ast
import os

def extract_code_blocks(file_path):
    """
    Extracts code blocks from a .qmd file.
    """
    code_blocks = []
    inside_code_block = False
    code_block = []

    with open(file_path, 'r', errors='ignore') as file:
        for line in file:
            if line.strip() == '```':
                if inside_code_block:
                    code_blocks.append('\n'.join(code_block))
                    code_block = []
                inside_code_block = not inside_code_block
            elif inside_code_block:
                code_block.append(line)
    
    return code_blocks

def find_dependencies_in_file(file_path):
    code_blocks = []
    if file_path.endswith('.qmd'):
        code_blocks = extract_code_blocks(file_path)
    else:
        with open(file_path, 'r', errors='ignore') as file:
            code_blocks.append(file.read())

    imports = set()
    for code in code_blocks:
        try:
            tree = ast.parse(code, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError as e:
            print(f"SyntaxError in {file_path}: {e}")
    return imports

def find_dependencies_in_directory(directory):
    dependencies = set()
    # Find all .py, .ipynb, and .qmd files
    files_to_process = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files if file.endswith(('.py', '.ipynb', '.qmd'))
    ]
    
    # Use tqdm to show the progress of processing files
    for file_path in tqdm(files_to_process, desc="Processing files"):
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

# %%
