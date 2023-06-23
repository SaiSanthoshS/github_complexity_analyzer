# GitHub Repository Analyzer

GitHub Repository Analyzer is a Python-based tool that analyzes a GitHub user's repositories to determine the most technically complex and challenging repository from their profile. It uses the GPT-3.5 language model and LangChain to assess each repository individually before identifying the most technically challenging one.

## Features

- Fetches a user's repositories from their GitHub user URL.
- Preprocesses code in repositories to handle large files and memory management.
- Utilizes prompt engineering for evaluating the technical complexity of code.
- Identifies the most technically complex repository using GPT.
- Provides GPT analysis justifying the selection.
- User-friendly web interface for input and result display.

## Installation

1. Clone the repository:
git clone https://github.com/your-username/github_complexity_analyzer.git


2. Install the required Python packages:
pip install -r requirements.txt


3. Set up your OpenAI API credentials by creating a `.env` file in the project root directory. Add the following lines to the file:
OPENAI_API_KEY=your-api-key
Replace `your-api-key` with your actual OpenAI API key.

## Usage

1. Start the Flask application: python main.py

2. Access the application by navigating to `http://localhost:5000` in your web browser.

3. Enter a GitHub user URL in the input field and click the "Analyze" button.

4. The application will analyze the repositories and display the most technically complex repository along with GPT analysis justifying the selection.

## Demo

Check out the [demo video](https://youtube.com/your-demo-video-url) showcasing the GitHub Repository Analyzer in action.






