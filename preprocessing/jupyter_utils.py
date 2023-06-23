import os
from preprocessing.file_utils import preprocess_code_file
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_client.kernelspec import NoSuchKernel

def convert_notebook_to_script(notebook_path, script_path):
    """Convert a Jupyter notebook to a Python script."""
    kernel_name = get_notebook_kernel(notebook_path)
    cmd = f"jupyter nbconvert --to python --execute --ExecutePreprocessor.kernel_name={kernel_name} --output {script_path} {notebook_path}"
    os.system(cmd)

def get_notebook_kernel(notebook_path):
    """Get the kernel name of a Jupyter notebook."""
    kernel_spec_manager = KernelSpecManager()
    try:
        kernel_spec = kernel_spec_manager.get_kernel_spec_for_nbconvert(notebook_path)
        return kernel_spec.language
    except NoSuchKernel:
        raise ValueError("Unable to determine the kernel for the notebook.")

def preprocess_jupyter_notebook(notebook_path, max_tokens):
    """Preprocess a Jupyter notebook by converting it to a script and truncating it if it exceeds the token limit."""
    script_path = notebook_path.replace('.ipynb', '.py')
    convert_notebook_to_script(notebook_path, script_path)
    preprocess_code_file(script_path, max_tokens)
    os.remove(notebook_path)

