import psutil
import os

def get_available_memory():
    """Get the available memory in bytes."""
    mem = psutil.virtual_memory()
    return mem.available

def is_memory_sufficient(file_size, memory_threshold):
    """Check if the available memory is sufficient to handle a file of given size."""
    available_memory = get_available_memory()
    return available_memory > file_size + memory_threshold

def delete_large_file(file_path):
    """Delete a large file from the file system."""
    os.remove(file_path)

def preprocess_large_file(file_path, max_file_size, memory_threshold):
    """Preprocess a large file by deleting it if it exceeds the size limit."""
    file_size = os.path.getsize(file_path)
    if file_size > max_file_size and not is_memory_sufficient(file_size, memory_threshold):
        delete_large_file(file_path)
