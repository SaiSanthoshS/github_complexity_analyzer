import os
from file_utils import preprocess_code_file

import nbformat
from nbconvert import PythonExporter

def convert_notebook_to_script(notebook_path, script_path):
    """Convert a Jupyter notebook to a Python script."""
    with open(notebook_path, 'r') as notebook_file:
        notebook = nbformat.read(notebook_file, as_version=nbformat.NO_CONVERT)

    exporter = PythonExporter()
    code, _ = exporter.from_notebook_node(notebook)

    with open(script_path, 'w') as script_file:
        script_file.write(code)

def preprocess_jupyter_notebook(notebook_path, max_tokens):
    """Preprocess a Jupyter notebook by converting it to a script and truncating it if it exceeds the token limit."""
    script_path = notebook_path.replace('.ipynb', '.py')
    convert_notebook_to_script(notebook_path, script_path)
    preprocess_code_file(script_path, max_tokens)
    os.remove(notebook_path)
