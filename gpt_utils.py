import openai
import requests
from preprocessing.file_utils import preprocess_code_file
from preprocessing.jupyter_utils import preprocess_jupyter_notebook
from preprocessing.memory_utils import preprocess_large_file

# Set up your OpenAI API credentials
openai.api_key = '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'

def generate_prompt(repository_name, code):
    """
    Generate a prompt for evaluating the technical complexity of a repository.
    Customize the prompt based on specific parameters for evaluation.
    """
    prompt = f"What are the technical complexities of the {repository_name} repository?\n"

    # Add specific parameters for evaluation
    prompt += "\n1. Code Quality: Evaluate the code quality of the repository."
    prompt += "\n2. Documentation Quality: Evaluate the documentation quality of the repository."
    prompt += "\n3. Readability: Evaluate the readability of the code in the repository."
    prompt += "\n4. Activity Level: Evaluate the activity level of the repository."
    prompt += "\n5. Community Engagement: Evaluate the community engagement of the repository."

    # Add the code for evaluation
    prompt += f"\n\nCode:\n{code}"

    prompt += "\n\nThe response should be strictly in the format 'Score: X and Reason: Y' with x being the score and y being the reason for that score with the above 5 parameters included\n"

    return prompt

def evaluate_repository(prompt):
    """Evaluate the technical complexity of a repository using the GPT-3.5 model."""

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

    # Process the response to extract the score and reason
    score, reason = extract_score_and_reason(response)

    return score, reason

def extract_score_and_reason(response):
    """
    Extract the score and reason from the response text.
    The response text should be in the format "Score: X and Reason: Y".
    Returns (0.0, '') if the response is empty or the score and reason cannot be extracted.
    """
    try:
        parts = response.split("and")
        score_str = parts[0].strip().split(":")[1].strip()
        reason_str = parts[1].strip().split(":")[1].strip()
        score = float(score_str)
        score = max(0, min(10, score))  # Limit the score between 0 and 10
        reason = reason_str
    except (ValueError, IndexError):
        score = 0.0  # Default score in case of error
        reason = ''

    return score, reason

def fetch_repositories(github_username):
    url = f'https://api.github.com/users/{github_username}/repos'
    response = requests.get(url)

    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        # Handle API request error
        return []