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
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from flask import send_from_directory

app = Flask(__name__,template_folder="templ")

ALLOWED_EXTENSIONS = {'xlsx', 'csv', 'xls'}
app.config['UPLOAD_FOLDER']="/uploads"
from flask import Flask, request, render_template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/num2text/', methods=['POST'])
def num_text():
    json_data = request.get_json()
    # Проверяем наличие необходимого ключа в запросе
    if 'number' not in json_data or 'series' not in json_data:
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/excel/', methods=['POST'])
def work_with_excel():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':#Если какой либо файл отправили
            uploaded_file.save(os.path.join(os.getcwd(),'uploads','file.'+uploaded_file.filename.rsplit('.', 1)[1].lower())) #'1'+uploaded_file.filename.rsplit('.', 1)[1].lower())) #os.getcwd() os.path.join(path, *paths)
            sheets=pd.read_excel('./uploads/file.'+uploaded_file.filename.rsplit('.', 1)[1].lower())
            buffer_array=[]
            for i,x in enumerate(sheets.values):
                if (type(x[0])==np.int64 and type(x[1])==np.int64 and len(str(x[0]))==4 and len(str(x[1]))==6):
                   buffer_array.append(check(x[0],x[1]))#sheets.values[2][i]=check(x[0],x[1])
            sheets["Вердикт"]=buffer_array
            sheets.to_excel('./uploads/file.'+uploaded_file.filename.rsplit('.', 1)[1].lower())
            #print(sheets)
            
        return send_from_directory(path='.', directory='uploads', filename='file.xlsx')#""#redirect(url_for('download')) #<a href="{{ url_for('download', filename="downloadFile.txt") }}">File</a>
    return render_template('index.html')



    
if __name__ == '__main__':
    app.run(debug=True)
