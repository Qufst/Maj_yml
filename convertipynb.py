import os
import subprocess


def convert_notebooks_to_scripts(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                script_path = os.path.splitext(notebook_path)[0] + ".py"
                try:
                    subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook_path, "--output", script_path], check=True)
                    print(f"Converted {notebook_path} to {script_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {notebook_path}: {e}")

if __name__ == "__main__":
    directory = "."  # Remplacez par le chemin de votre répertoire contenant les fichiers .ipynb si nécessaire
    convert_notebooks_to_scripts(directory)
