# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 20:48:21 2022

@author: liali
"""
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

def get_series():
    value=''
    while not match("^[0-9]{4}$", value):
        value=input('Введите серию паспорта')
    return value
def get_number():
    value=''
    while not match("^[0-9]{6}$", value):
        value=input('Введите номер паспорта')
    return value

def check(series,number):
 TRIGGER_LINE="Cреди недействительных не значится"
 ATTEMPTS=3
 model_name='final.h5'
 save_dir=os.getcwd() 
 model_path = os.path.join(save_dir, model_name)
 model = keras.models.load_model(model_path)
 

 finish=False

 #soup = BeautifulSoup(r.content, features="html.parser")
 #print(soup)

 serie=series#get_series()
 number=number#get_number()
 counter=0
 while finish==False:
     counter=counter+1
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
     if (counter==ATTEMPTS):
         return "Произведено максимальное количество попыток"
     if ('form_DOC_SERIE' not in r.text)==True:
         finish=True
  

 if TRIGGER_LINE in soup.text:
     return True#print('С паспортом всё впорядке')
 else:
     return False#print('С паспортом проблемы')
        
#print(check(11111,11111))

