from flask import Flask

app = Flask(__name__)
app.template_folder = 'template'

from app import routes
