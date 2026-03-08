from argparse import Action
from datetime import date

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
    if intent_name == "country":
        return countries(req, intent_name)
    elif intent_name=="number":
        return contact(req, intent_name)
    elif intent_name=="verification":
        return verify(req, intent_name, result2)
    elif intent_name=="beneficiary":
        return certificate(req, intent_name, result4)
    elif intent_name=="symptoms":
        return symp(req,intent_name)
    elif intent_name=="pincode":
        return info(req,intent_name)
    elif intent_name=="v_date":
        return slot(req,intent_name,pc1)
    
def countries(req, intent_name):
    country = req["queryResult"]["parameters"]["countries"]
    #print(country)
    action = req["queryResult"]["action"]
    
    #fetching data from API
    url = "https://covid-19-tracking.p.rapidapi.com/v1/"+country
    headers = {
            'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
            'x-rapidapi-key': "ff3b442cd4mshb8dc83e4857e99ap11954djsn4a0058b2a201"
            }
    response = requests.request("GET", url, headers=headers)
    result1=response.json()
    print(result1)
    if action == "TextResponse":
        return {

            "fulfillmentText":  "Active cases: "+result1['Active Cases_text']+'\n'+
                                "New Cases: "+result1['New Cases_text']+'\n'+
                                "New Deaths: "+result1['New Deaths_text']+'\n'+
                                "Total Cases: "+result1["Total Cases_text"]+'\n'+
                                "Total Deaths: "+result1["Total Deaths_text"]+'\n'+
                                "Total Recovered: "+result1["Total Recovered_text"]+'\n'+
                                "Last Update: "+result1["Last Update"]

        }


def contact(req, intent_name):
    global result2
    no = req["queryResult"]["parameters"]["phone-number"]
    #action = req["queryResult"]["action"]
    print(no)
    #Generate OTP
    url = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
        }
    phone='{"mobile":"'+no+'"}'
    print(phone)
    result2 = requests.post(url, data=phone, headers=headers)
    print(result2.text)
    result2=result2.json()
    return result2

def verify(req, intent_name,result2):
    global result4
    
    #convert otp to sha256
    otp = req["queryResult"]["parameters"]["otp"]
    hashobj = hashlib.sha256(bytes(otp, 'utf-8'))
    val = int.from_bytes(hashobj.digest(), 'big')
    result3='%064x' % val
  
  
    #Generate token
    url = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
        }
    tkn='{"otp":'+'"'+result3+'"'+',"txnId":'+'"'+result2['txnId']+'"'+'}'
    print(tkn)
    res = requests.post(url, data=tkn, headers=headers)
    result4=res.json()
    print(result4)
    return result4


def certificate(req, intent_name, result4):
    id = req["queryResult"]["parameters"]["reference"]
    action = req["queryResult"]["action"]
    print(id)
    #generate pdf
    url = "https://cdn-api.co-vin.in/api/v2/registration/certificate/public/download?beneficiary_reference_id="+id
    val='Bearer '+result4['token']
    print(val)
    headers = {
        "accept": "application/pdf",
        "Authorization": val
        }
    print(headers)
    res=requests.get(url, headers=headers)
    print(res)
    name=id+'.pdf'
    if res.status_code==200:
        with open(name,'wb') as f:
            f.write(res.content)
    if action == "TextResponse":
        return {
            "fulfillmentText": "Success"
            }
def symp(req,intent_name):
    action=req["queryResult"]["action"]
    if action=="TextResponse":
        return {
            "fulfillmentText": "Most common symptoms:"+"\n"+"1.Fever"+"\n"+"2.Cough"+"\n"+"3.Tiredness"+"\n"+"4.Loss of taste or smell"+"\n\n"
            +"Least common symptoms:"+"\n"+"1.Sore throat"+"\n"+"2.Headache"+"\n"+"3.Aches and Pain"+"\n"+"4.Diarrhoea"+"\n"+"5.Rash on skin"+"\n"+
            "6.Red or irritated eyes"+"\n\n"+"Serious symptoms:"+"\n"+"1.Difficulty breathing "+"\n"+"2.Loss of speech"                      
        }

def info(req,intent_name):
    global pc1

    action=req["queryResult"]["action"]
    p=req["queryResult"]["parameters"]["code"]
    pc1=str(p)
    return pc1

def slot(req,intent_name,pc1):
    global dt

    action=req["queryResult"]["action"]
    dt=req["queryResult"]["parameters"]["date-time"]
    dt1=str(dt)
    dt1=dt1.split('T')
    tmp=dt1[0].split('-')
    date_obj=tmp[2]+"-"+tmp[1]+"-"+tmp[0]

    print("date: ",date_obj)
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+pc1+"&date="+date_obj
    print(date_obj)
    response = requests.request("GET", url)
    result1=response.json()
    print(result1)
    st1=""
    st2=""
    st3=""
    st4=""
    li2=[]
    for i in range(len(result1["sessions"])):
        if (result1["sessions"][i]["name"] not in st1):
            st1=st1+"\n"+result1["sessions"][i]["name"]
        if (str(result1["sessions"][i]["available_capacity"]) not in st3):
            st2=st2+"\n"+(str(result1["sessions"][i]["available_capacity"]))
        if (result1["sessions"][i]["vaccine"] not in st4):
            st4=st4+"\n"+(result1["sessions"][i]["vaccine"])
        if (result1["sessions"][i]["slots"] not in li2):
            li2.append(result1["sessions"][i]["slots"])


######print(*li1,sep="\n")
##st=str(li2[0]).strip('[]')
##st1=st.strip("'")
    st3="09:00AM-10:00AM"+"\n"+"10:00AM-11:00AM"+"\n"+"11:00AM-12:00PM"+"\n"+"12:00PM-02:00PM"
    print(st1,st4,st2)
    print(st3)
    print(li2)
    if action=="TextResponse":
        return {
           "fulfillmentText" :"Hospital Detalis:"+ st1+"\n\n"+"Slot Timing: \n"+st3+"\n"+"\n"+"Vaccine Availabe: "+st4
        }
    


    ######print(*li1,sep="\n")
    ##st=str(li2[0]).strip('[]')
    ##st1=st.strip("'")
    
    




 

if __name__ == '__main__':
    app.run(port=5020, debug=True)