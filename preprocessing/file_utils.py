import os

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)

def delete_file(file_path):
    """Delete a file from the file system."""
    os.remove(file_path)

def get_file_extension(file_path):
    """Get the extension of a file."""
    return os.path.splitext(file_path)[1]

def is_code_file(file_path):
    """Check if a file is a code file based on its extension."""
    valid_extensions = ['.py', '.ipynb']
    file_extension = get_file_extension(file_path)
    return file_extension.lower() in valid_extensions

def preprocess_code_file(code, max_tokens):
    """Preprocess a code file by truncating it if it exceeds the token limit."""
    code_lines = code.split('\n')
    if len(code_lines) > max_tokens:
        truncated_code = '\n'.join(code_lines[:max_tokens])
        return truncated_code

    return code

