from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import io
import os
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas as rotas da sua aplicação

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/describe', methods=['POST'])
def describe_image():

    # Verifica se a requisição contém dados
    if 'image' not in request.json:
        return jsonify({'error': 'No image data sent in request body'}), 400
    
    if 'context' not in request.json:
        context = 'Descreva com detalhes'

    context = request.json['context']
    try:
        # Decodifica a base64 para obter os bytes da imagem
        image_data = base64.b64decode(request.json['image'])
        
        # Converte os bytes em um objeto de imagem
        image = Image.open(io.BytesIO(image_data))

        response = model.generate_content([context, image])
        response.resolve()

        # Retorna a descrição da imagem como JSON
        return jsonify({'description': response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
