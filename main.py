from flask import Flask, render_template, request
from gpt_utils import evaluate_repository

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    github_url = request.form['github_url']
    
    # Extract the repository name from the GitHub URL
    repository_name = extract_repository_name(github_url)
    
    # Evaluate the technical complexity of the repository
    complexity = evaluate_repository(repository_name)
    
    return render_template('result.html', repository_name=repository_name, complexity=complexity)

def extract_repository_name(github_url):
    # Remove the trailing slash if present
    if github_url.endswith('/'):
        github_url = github_url[:-1]

    # Split the URL by the slash character
    url_parts = github_url.split('/')

    # Extract the repository name from the URL
    repository_name = url_parts[-1]

    return repository_name


if __name__ == '__main__':
    app.run(debug=True)
