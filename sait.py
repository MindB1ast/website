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

app = Flask(__name__)
def load_data_one(path):
    IMG_ROW, IMG_COLS = 60, 198
    x_test = []
    names=[]
    
    # r=root, d=directories, f = files  
    for r, d, f in os.walk(path):
        for fl in f:
            if '.jpg' in fl:
                flr = fl.split('.')[0]
                names.append(flr)
                img = cv2.imread(os.path.join(r, fl))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (int(IMG_COLS/2), int(IMG_ROW/2)), interpolation=cv2.INTER_AREA)
                img = np.reshape(img, (img.shape[0], img.shape[1], 1))
                x_test.append(img)
    return np.array(x_test),np.array(names)

model_name='final.h5'
save_dir=os.getcwd() 
model_path = os.path.join(save_dir, model_name)
model = keras.models.load_model(model_path)
finish=False


@app.route('/num2text/', methods=['POST'])
def num_text():
    finish=False
    json_data = request.get_json()
    # Проверяем наличие необходимого ключа в запросе
    if 'number' not in json_data:
        return jsonify(str='something wrong')
    # Достаем пришедшие данные из запроса
    number = json_data['number']
    serie = json_data['series']
    while finish==False:

     s=requests.session()
     req = s.get('http://services.fms.gov.ru/services/captcha.jpg', stream=True)

     req.raise_for_status()
     with open('capthcas\captcha.jpg', 'wb') as fd:
          for chunk in req.iter_content(chunk_size=50000):
              #print(f'Received a Chunk')
              fd.write(chunk)
             
            
    
     x_test,names=load_data_one('capthcas')
     output=model.predict(x_test)
     x_test=[]
     names=[]
     #0-номер цифры в капче 1-номер входного значения  2-вероятность цифры(0-9)
     answ=[]
     for i in range(int(np.size(output[0])/np.size(output[0][0]))):
         strq=''
         for q in range(6):
             #print(np.argmax(output[q][i]))
             strq+=str(np.argmax(output[q][i]))
         answ.append(strq)
     login_details=answ[0]
     
     
     params={'sid':2000,
                        'form_name':'form',
                        'DOC_SERIE':serie,
                        'DOC_NUMBER':number,
                        'captcha-input':login_details
             }
     r = s.post('http://services.fms.gov.ru/info-service.htm',params=params)           
     soup = BeautifulSoup(r.content, features="html.parser")
     #print(soup)
     print(login_details)
     #print('form_DOC_SERIE' not in r.text)
     if ('form_DOC_SERIE' not in r.text)==True:
         finish=True








    text=str("Cреди недействительных не значится" in soup.text)
    
    # Начало блока по обработке пришедших данных. Здесь пишем свой код
    #text = num2words(number, lang='ru')
    # Конеч блока обработки данных

    return jsonify(str=text)


if __name__ == '__main__':
    app.run(debug=True)
