from argparse import Action
from ast import In
from datetime import date
import re
from urllib import response
from flask import Flask
from flask import request
from flask import make_response
import json
import requests
from datetime import datetime

import hashlib
#global result2

#flask set up
app = Flask(__name__)
app.secret_key = "abc"

@app.route('/', methods=["GET","POST"])
def service():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    if intent_name == "s_breath":
        return breaths(req,intent_name)
    elif intent_name == "s1_cough":
        return coughs(req,intent_name)
    elif intent_name == "s1_age":
        return coughs1(req,intent_name)
    elif intent_name == "s_fever":
        return fev(req,intent_name)
    elif intent_name == "s_abroad":
        return abr(req,intent_name)
    elif intent_name == "s_confirmed":
        return conf(req,intent_name)
    elif intent_name == "s_gender":
        return gend(req,intent_name)
    elif intent_name == "s_headache":
        return head(req,intent_name)
    elif intent_name == "conclusion":
        return result(req,intent_name,para1,para2,para3,para4,para5,para6,para7,para8,para81)




def breaths(req,intent_name):
    global para1
    short=req["queryResult"]["parameters"]["breath"]
    action = req["queryResult"]["action"]
    if short=="yes, I experience shortness of breath":
        para1=str(1)
    else:
        para1=str(0)
    print(short,para1)
    return para1

def coughs(req,intent_name):
    global para2
    global para3
    cou=req["queryResult"]["parameters"]["above_60"]
    action = req["queryResult"]["action"]
    if cou=="yes":
        para2=str(1)
        para3=str(0)
    print(cou)
    print(para2,para3)
    return para2,para3

def coughs1(req,intent_name):
    cou1=req["queryResult"]["parameters"]["above_60"]
    action = req["queryResult"]["action"]
    if cou1=="Yes, I'm below 60":
        para2=str(0)
        para3=str(1)
    print(cou1)
    print(para2,para3)
    return para2,para3


def fev(req,intent_name):
    global para4
    fevs=req["queryResult"]["parameters"]["cough"]
    if fevs == "yes, i have cough":
        para4=str(1)
    else:
        para4=str(0)
    print("fevs",para4)
    return para4

def abr(req,intent_name):
    global para5
    abrs=req["queryResult"]["parameters"]["fever"]
    if abrs == "yes, i feel feverish":
        para5=str(1)
    else:
        para5=str(0)
    print("abrs",para5)
    return para5

def conf(req,intent_name):
    global para6
    confs=req["queryResult"]["parameters"]["abroad"]
    if confs == "No, I do not travel much":
        para6=str(1)
    else:
        para6=str(0)
    print("confs ",para6)
    return para6

def gend(req,intent_name):
    global para7
    gends=req["queryResult"]["parameters"]["confirmed"]
    if gends == "Yes, I have been in contact":
        para7=str(1)
    else:
        para7=str(0)
    print("gends ",para7)
    return para7

def head(req,intent_name):
    global para8,para81

    heads=req["queryResult"]["parameters"]["gender"]
    print(heads)
    if heads == "Female":
        para8 = str(1)
        para81 = str(0)
    elif heads == "Male":
        para81 = str(1)
        para8 = str(0)

    print(para8,para81)
    return para8, para81

def result(req,intent_name,para1,para2,para3,para4,para5,para6,para7,para8,para81):
    
    action = req["queryResult"]["action"]
    url = "https://coronavirus-symptoms-predictor1.p.rapidapi.com/"
   
    if para1!="":
        pass
    elif para1=="":
        para1=0
    if para2!="":
        pass
    elif para2=="":
        para2=0
    if para3!="":
        pass
    elif para3=="":
        para3=0
    if para4!="":
        pass
    elif para4=="":
        para4=0
    if para5!="":
        pass
    elif para5=="":
        para5=0
    if para6!="":
        pass
    elif para6=="":
        para6=0
    if para7!="":
        pass
    elif para7=="":
        para7=0
    if para8!="":
        pass
    elif para8=="":
        para8=0
    print(para1,para2,para3,para4,para5,para6,para7,para8,para81)

    querystring = {"has_shortness_of_breath":para1,"above_60_no":para2,"above_60_yes":para3,"has_cough":para4,"has_fever":para5,"is_male":para81,"has_been_abroad":para6,
                "contact_with_confirmed":para7,"is_female":para8,"has_head_ache":"0"}

    headers = {
        "X-RapidAPI-Host": "coronavirus-symptoms-predictor1.p.rapidapi.com",
        "X-RapidAPI-Key": "ff3b442cd4mshb8dc83e4857e99ap11954djsn4a0058b2a201"
    }

    response = requests.request("POST", url, headers=headers, params=querystring)

    result=dict(response.json())
    results=""
    if result["has_covid_symptoms"]=='0':
        results="You don't seem to have any covid related symptoms,but please continue to wear mask and follow covid 19 protocols"
    elif result["has_covid_symptoms"]=='1':
        results="It seems that you may have covid. Isolate yourself and be safe."


    if action=="TextResponse":
        return {
           "fulfillmentText" : results
        }



    




if __name__ == '__main__':
    app.run(port=5000, debug=True)