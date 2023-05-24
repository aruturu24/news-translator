from flask import Flask, jsonify, render_template
import requests
from deep_translator import GoogleTranslator

API_URL = 'https://inshorts.deta.dev/news?category=science'


class Noticia:
    def __init__(self, json):
        self.autor = json.get('author')
        self.titulo = self.traduzir(json.get('title'))
        self.conteudo = self.traduzir(json.get('content'))
        self.data = self.traduzir(json.get('date'))
        self.fonte = json.get('readMoreUrl')

    def traduzir(self, texto):
        return GoogleTranslator(
            source='auto', target='pt'
        ).translate(texto)

    def __str__(self):
        jsonNoticia = {
            "autor": self.autor,
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "data": self.data,
            "fonte": self.fonte
        }
        return str(jsonNoticia)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/noticias', methods=['GET'])
def noticias():
    apiNoticias = requests.get(API_URL).json()
    brNoticias = []
    for noticia in apiNoticias['data']:
        brNoticias.append(str(Noticia(noticia)))

    return jsonify(brNoticias)


if __name__ == "__main__":
    app.run()
