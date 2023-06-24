from flask import Flask, render_template, request
from rating_utils import (
    evaluate_code_quality,
    evaluate_documentation,
    evaluate_activity_level,
    evaluate_community_engagement
)
import requests

app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    github_username = request.form.get('github_username')

    # Fetch repositories based on the GitHub username
    repositories = fetch_repositories(github_username)

    # Evaluate the metrics for each repository
    metrics_results = {}
    for repository_name in repositories:
        code_quality_score = evaluate_code_quality(repository_name)
        documentation_score = evaluate_documentation(repository_name)
        activity_level_score = evaluate_activity_level(repository_name)
        community_engagement_score = evaluate_community_engagement(repository_name)

        # Calculate the overall rating score
        overall_score = calculate_overall_score(
            code_quality_score,
            documentation_score,
            activity_level_score,
            community_engagement_score
        )

        metrics_results[repository_name] = {
            'Code Quality': code_quality_score,
            'Documentation': documentation_score,
            'Activity Level': activity_level_score,
            'Community Engagement': community_engagement_score,
            'Overall Score': overall_score
        }

    return render_template('result.html', repositories=metrics_results)


def fetch_repositories(github_username):
    # Fetch repositories based on the GitHub username
    url = f"https://api.github.com/users/{github_username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        return []

def calculate_overall_score(code_quality_score, documentation_score, activity_level_score, community_engagement_score):
    # Placeholder logic to calculate the overall rating score
    # Your code here
    # Example: Assume a simple average of the individual scores
    return (code_quality_score + documentation_score + activity_level_score + community_engagement_score) / 4


if __name__ == '__main__':
    app.run(debug=True)
