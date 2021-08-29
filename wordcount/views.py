from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import json
import operator
import time
import uuid
from datetime import datetime
from decimal import Decimal
import requests
import datefinder
from operator import itemgetter
import feedparser
from io import StringIO
import io
import base64
import urllib
import numpy as np
from typing import Dict
import pymongo
import pandas as pd
import math
myclient = pymongo.MongoClient("mongodb+srv://vladha:"+urllib.parse.quote("Carramba123@")+"@cluster0.swken.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient["Tracker"]
mycol = mydb["Time"]

#'date', 'hours', 'notes', 'name', 'function', 'task_id',       'function_code', 'client_id', 'client', 'group_id', 'group'


#query={'date':'25/08/21'}
query={}


def datestr(row):
    dt=row['date']
    result=dt[3:][:2]+"/"+dt[:2]+"/"+dt[-2:]
    #print(type(dt))
    #print(dt)
    #print(result)
    return result



def home(request):
    if "GET" == request.method:

        date1 = request.GET.get('from')
        if date1:
            date1=date1[:6]+date1[-2:]


        date2 = request.GET.get('to')
        if date2:
            date2=date2[:6]+date2[-2:]

        search = request.GET.get('search')
        print(date1,date2,search)

       
    timedatafull=list(mycol.find(query))
    df=pd.DataFrame(timedatafull)
    
    
    df['key']=df['group']+"-"+df['function']+df['client']+df['name']
    df['key']=df['key'].fillna("nothing")
    
    df['strdt']=df.apply(datestr,axis=1)
    #print(df)

    
    if search:
        df=df[df['key'].str.contains(search,case=False)]
    
    if date1 and len(date1)>0:
        df=df[df['strdt']>=date1]
    
    if date2 and len(date2)>0:
        df=df[df['strdt']<=date2]

    df['activity']=df['group']+"-"+df['function']


    df1=df.groupby(['activity','name'])['hours'].sum().reset_index().sort_values(by=['activity','hours'],ascending=False)
    d1 = json.loads(df1.to_json(orient ='records') )
    
    
    df2=df.groupby(['group','name'])['hours'].sum().reset_index().sort_values(by=['group','hours'],ascending=False)
    d2 = json.loads(df2.to_json(orient ='records') )
    
    
    df3=df.groupby(['group'])['hours'].sum().reset_index().sort_values(by=['hours'],ascending=False)
    d3 = json.loads(df3.to_json(orient ='records') )
    
    return render(request, 'home.html', {'d1':d1,'d2':d2,'d3':d3})


