import json
import re
import os
from nbformat import v4 as nbf

def read_qmd_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def parse_qmd_content(content):
    cells = []
    code_blocks = re.findall(r'```{python}(.+?)```', content, re.DOTALL)
    text_blocks = re.split(r'```{python}.*?```', content, re.DOTALL)
    
    for i, text in enumerate(text_blocks):
        if text.strip():
            cells.append(nbf.new_markdown_cell(text.strip()))
        if i < len(code_blocks):
            cells.append(nbf.new_code_cell(code_blocks[i].strip()))
    
    return cells

def split_cells_to_notebooks(cells, base_output_path):
    for i, cell in enumerate(cells):
        nb = nbf.new_notebook()
        nb['cells'] = [cell]
        output_path = f"{base_output_path}_part_{i+1}.ipynb"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)

def convert_qmd_to_ipynb(input_path, base_output_path):
    content = read_qmd_file(input_path)
    cells = parse_qmd_content(content)
    split_cells_to_notebooks(cells, base_output_path)

def convert_all_qmd_in_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".qmd"):
                input_path = os.path.join(root, file)
                base_output_path = os.path.join(output_directory, os.path.splitext(file)[0])
                convert_qmd_to_ipynb(input_path, base_output_path)

# utilisation
input_directory = '/'  # Remplacez par le chemin de votre répertoire contenant les fichiers .qmd
output_directory = 'ipynb/'  # Remplacez par le chemin de votre répertoire de sortie pour les fichiers .ipynb
convert_all_qmd_in_directory(input_directory, output_directory)
