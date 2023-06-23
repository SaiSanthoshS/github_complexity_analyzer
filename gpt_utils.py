import openai
from preprocessing.file_utils import preprocess_code_file
from preprocessing.jupyter_utils import preprocess_jupyter_notebook
from preprocessing.memory_utils import preprocess_large_file

# Set up your OpenAI API credentials
openai.api_key = 'YOUR_API_KEY'

def generate_prompt(repository_name):
    """Generate a prompt for evaluating the technical complexity of a repository."""
    prompt = f"What are the technical complexities of the {repository_name} repository?"
    return prompt

def evaluate_repository(repository_name):
    """Evaluate the technical complexity of a repository using the GPT-3.5 model."""
    prompt = generate_prompt(repository_name)

    # Set the parameters for the completion
    completion_kwargs = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.6,
        'n': 1,
        'stop': None
    }

    # Generate the completion using the GPT-3.5 model
    completion_response = openai.Completion.create(**completion_kwargs)

    # Extract the generated response
    response = completion_response.choices[0].text.strip()

    return response
