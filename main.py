from flask import Flask, render_template, request
from gpt_utils import evaluate_repository, fetch_repositories, generate_prompt
import requests
from preprocessing.file_utils import preprocess_code_file
from preprocessing.jupyter_utils import preprocess_jupyter_notebook
from preprocessing.memory_utils import preprocess_large_file

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    github_username = request.form.get('github_username')

    # Fetch repositories based on the GitHub username
    repositories = fetch_repositories(github_username)

    # Evaluate the technical complexity of each repository
    complexity_results = []

    for repository_name in repositories:
        # Fetch the code of the repository (replace this with your code to fetch the code from the repository)
        code = fetch_repository_code(repository_name)

        # Generate the prompt with code for evaluation
        prompt = generate_prompt(repository_name, code)

        # Evaluate the technical complexity using GPT
        score, reason = evaluate_repository(prompt)

        # Add repository details to the results
        result = {
            'repository_name': repository_name,
            'score': score,
            'reason': reason,
            'repo_link': f'https://github.com/{github_username}/{repository_name}'
        }
        complexity_results.append(result)

    return render_template('result.html', repositories=complexity_results)

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
                file_name = item['name']
                file_extension = file_name.rsplit('.', 1)[-1].lower()

                # Preprocess the code file based on its extension
                if file_extension == 'ipynb':
                    code = fetch_code_from_url(file_url)
                    if code is not None:
                        preprocessed_code = preprocess_jupyter_notebook(code)
                        code_files.append((file_name, preprocessed_code))
                else:
                    code = fetch_code_from_url(file_url)
                    if code is not None:
                        if len(code) > MAX_TOKENS_THRESHOLD:
                            preprocessed_code = preprocess_large_file(code)
                        else:
                            preprocessed_code = preprocess_code_file(code)
                        code_files.append((file_name, preprocessed_code))

        return code_files
    else:
        # Handle request error
        return []

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

if __name__ == '__main__':
    app.run(debug=True)

