import openai
import requests

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

    print(response)

    # Process the response to extract the score and reason
    score, reason = extract_score_and_reason(response)

    # Check if the keys exist in the response
    score_keys = ['Code Quality', 'Documentation Quality', 'Readability', 'Activity Level', 'Community Engagement']
    reason_keys = ['Code Quality', 'Documentation Quality', 'Readability', 'Activity Level', 'Community Engagement']

    # Create the result dictionary
    result = {}
    for key in score_keys:
        if key in score:
            result[key] = {'score': score[key], 'reason': reason[key]}
        else:
            result[key] = {'score': None, 'reason': None}

    print(result)

    return result

def extract_score_and_reason(response):
    """
    Extract the score and reason for each criterion from the response text.
    The response text should be in the format:
    "1. Code Quality: Score: X and Reason: Y
    2. Documentation Quality: Score: X and Reason: Y
    3. Readability: Score: X and Reason: Y
    4. Activity Level: Score: X and Reason: Y
    5. Community Engagement: Score: X and Reason: Y"
    Returns a dictionary containing the scores and reasons for each criterion.
    """
    scores = {}
    reasons = {}

    try:
        # Split the response into individual criteria
        criteria_list = response.split('\n')

        # Process each criterion
        for criterion in criteria_list:
            parts = criterion.strip().split(":")
            criterion_name = parts[0].strip()
            score_str = parts[1].split("Score:")[1].strip()
            reason_str = parts[2].split("Reason:")[1].strip()

            score = float(score_str)
            score = max(0, min(10, score))  # Limit the score between 0 and 10

            scores[criterion_name] = score
            reasons[criterion_name] = reason_str

    except (ValueError, IndexError):
        # Handle parsing errors
        scores = {}
        reasons = {}

    return scores, reasons




def fetch_repositories(github_username):
    url = f'https://api.github.com/users/{github_username}/repos'
    response = requests.get(url)

    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        # Handle API request error
        return []

def fetch_repository_code(repository_name):
    """
    Fetch the code from a given repository.
    Replace this function with your code to fetch the code from the repository.
    """
    # Make a GET request to fetch the repository code
    url = f"https://api.github.com/repos/{repository_name}/contents"
    response = requests.get(url)
    MAX_TOKENS_THRESHOLD = 1024

    if response.status_code == 200:
        contents = response.json()
        code_files = []

        for item in contents:
            if item['type'] == 'file':
                file_url = item['download_url']
                code = fetch_code_from_url(file_url)
                if code is not None:
                    code_files.append(code)

        return "\n".join(code_files)

    else:
        # Handle request error
        return ""

def fetch_code_from_url(file_url):
    """
    Fetch the code content from the given URL.
    Replace this function with your code to fetch the code content.
    """
    response = requests.get(file_url)

    if response.status_code == 200:
        code = response.text
        return code
    else:
        # Handle request error
        return None
