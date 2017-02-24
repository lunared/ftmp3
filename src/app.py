from flask import Flask
from . import song

app = Flask(__name__,
            template_folder='../templates')
app.config.from_object('src.settings')
