from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

from main import *

if __name__ == '__main__':
    app.run(debug=True)