from flask import Flask, render_template, request
from gpt_utils import evaluate_repository, fetch_repositories, generate_prompt, fetch_repository_code, fetch_code_from_url
import requests
from preprocessing.file_utils import is_code_file, preprocess_code_file
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
    complexity_results = {}
    max_score = 0
    most_complex_repository = None

    for repository_name in repositories:
        # Fetch the code of the repository (replace this with your code to fetch the code from the repository)
        code = fetch_repository_code(repository_name)

        # Preprocess the code based on its size
        if len(code) > 10_000:
            code = preprocess_large_file(code)
        elif code.endswith('.ipynb'):
            code = preprocess_jupyter_notebook(code, max_tokens=600)
        else:
            code = preprocess_code_file(code, max_tokens=600)

        # Generate the prompt with code for evaluation
        prompt = generate_prompt(repository_name, code)

        # Evaluate the technical complexity using GPT
        result = evaluate_repository(prompt)

        # Update the complexity results
        complexity_results[repository_name] = result

        # Update the most complex repository
        avg_score = sum(result[key]['score'] for key in result if result[key]['score'] is not None) / len(result)
        if avg_score > max_score:
            max_score = avg_score
            most_complex_repository = repository_name

        # Update the average score in the result dictionary
        result['Average Max Score'] = avg_score

    return render_template('result.html', repositories=complexity_results, most_complex=most_complex_repository, username=github_username)


if __name__ == '__main__':
    app.run(debug=True)
