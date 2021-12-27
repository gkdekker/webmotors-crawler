#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#to dos
#clean code
#colocar parametros de pesquisa

import requests
import unicodedata
import json
import pandas as pd
import time
import random
from requests.models import Response

def turnPages():
    cars = []
    page = 1
    webmotors = getCars(page)
    while len(webmotors['SearchResults']) == 24:
        cars.extend(treatCars(webmotors['SearchResults']))
        page +=1
        time.sleep(random.randint(2,4))
        print(len(cars),page)
        webmotors = getCars(page)
    if len(webmotors['SearchResults']) != 0:
        cars.extend(treatCars(webmotors['SearchResults']))
        print(len(cars),page)
    doCSV(cars)

def getCars(page):
    url = 'https://www.webmotors.com.br/api/search/car?url=https://www.webmotors.com.br/carros%2Fsc-itapema%3Festadocidade%3DSanta%2520Catarina%2520-%2520Itapema%26tipoveiculo%3Dcarros%26localizacao%3D-27.126343%2C-48.6086348x50km%26kmate%3D120000%26precoate%3D100000&actualPage=' + str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    response = requests.request("GET", url,headers=headers)
    return json.loads(response.content)

def treatCars(carList):
    index = 0
    treatedCars = []
    for car in carList:
        try:
            fipe = car['FipePercent']
        except:
            fipe = 666

        make = unicodedata.normalize("NFD",car['Specification']['Make']['Value']).encode("ascii", "ignore")
        model = unicodedata.normalize("NFD",car['Specification']['Model']['Value']).encode("ascii", "ignore")
        version = unicodedata.normalize("NFD",car['Specification']['Version']['Value']).encode("ascii", "ignore")
        ports = car['Specification']['NumberPorts']
        anoFabricacao = int(car['Specification']['YearFabrication'])
        anoModelo = int(car['Specification']['YearModel'])
        Id = car['UniqueId']
        link = 'https://www.webmotors.com.br/comprar/' + make + '/' + model + '/' + str(version).replace(' ','-',) + '/' + ports + '-portas/' + str(anoFabricacao) + '-' + str(anoModelo) + '/' + str(Id)
        treatedCar = {
            'Ano Fabricacao' : int(anoFabricacao),
            'Ano Modelo' : int(anoModelo),
            'Cidade' : car['Seller']['City'],
            'Cor' : car['Specification']['Color']['Primary'],
            'Fipe' : fipe,
            'Id' : Id,
            'KM' : int(car['Specification']['Odometer']),
            'Marca' : make,
            'Modelo' : model,
            'Tipo Vendedor' : car['Seller']['SellerType'],
            'Transmissao' : car['Specification']['Transmission'],
            'Valor' : int(car['Prices']['Price']),
            'Versao' : version,
            'Link' : link
        }
        treatedCars.append(treatedCar)
        index +=1
    return treatedCars

def doCSV(cars):
    df = pd.DataFrame(data=cars)
    column_names = ['Id','Fipe','Marca','Modelo','Valor','Ano Fabricacao','Ano Modelo','KM','Transmissao','Cor','Versao','Cidade','Tipo Vendedor','Link']
    mydf = df.reindex(columns=column_names)
    mydf.to_csv(r'WebmotorsCars.csv', encoding='utf-8',index=False) 

turnPages()