from flask import Flask
import google.generativeai as genai
import PIL.Image

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'