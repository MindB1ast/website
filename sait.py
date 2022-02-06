from flask import Flask, request, jsonify
#from num2words import num2words
import requests
from bs4 import BeautifulSoup
import os
import itertools
import tensorflow
import os
import cv2
import numpy as np
import keras
from keras.models import Sequential, Model
from re import match
from check import check,load_data_one

app = Flask(__name__,template_folder="templ")


from flask import Flask, request, render_template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/num2text/', methods=['POST'])
def num_text():
    json_data = request.get_json()
    # Проверяем наличие необходимого ключа в запросе
    if 'number' not in json_data:
        return jsonify(str='something wrong')
    # Достаем пришедшие данные из запроса
    number = json_data['number']
    serie = json_data['series']
    text=check(serie,number)
    #text=str("Cреди недействительных не значится" in soup.text)
    
    # Начало блока по обработке пришедших данных. Здесь пишем свой код
    #text = num2words(number, lang='ru')
    # Конеч блока обработки данных

    return jsonify(str=text)


if __name__ == '__main__':
    app.run(debug=True)
