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
    kernel_spec = kernel_spec_manager.find_kernel_specs().get('python3')  # Replace 'python3' with the appropriate kernel name
    if kernel_spec is not None:
        return kernel_spec.language
    else:
        raise ValueError("Unable to determine the kernel for the notebook.")


def preprocess_jupyter_notebook(notebook_code, max_tokens):
    """Preprocess a Jupyter notebook code by converting it to a script and truncating it if it exceeds the token limit."""
    script_path = "temp_script.py"
    with open(script_path, 'w') as script_file:
        script_file.write(notebook_code)

    preprocess_code_file(script_path, max_tokens)
    os.remove(script_path)


