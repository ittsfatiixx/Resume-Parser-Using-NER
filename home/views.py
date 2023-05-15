from django.shortcuts import render

import pandas as pd
import os
# Create your views here.
label_list=["ROWID","NAME","DESIGNATION","LOCATION","COMPANIES WORKED AT","SKILLS","COLLEGE NAME","DEGREE","GRADUATION YEAR","EMAIL ADDRESS","STATUS"]
    

def evaluate(df_source):
    # df_source=df_source.set_index('ROWID')
    data=df_source.to_dict()
    skill_set=[]
    for i in df_source.SKILLS:  
        skill_set.append(i)
    '''hardcoded Required skills, can be taken as input'''   
    req_skills=['cloud','.net','sql']
    ids=[id for id in df_source.index]
    top_ids=[]
    rej_ids=[]
    for id in ids:
        skill_count=0
        for rskill in req_skills:
            if rskill in data['SKILLS'][id]:
                skill_count+=1
        if skill_count>=2:
            df_source['STATUS'][id]='top'
            data['STATUS'][id]='top'
            top_ids.append(id) 
        else:
            df_source['STATUS'][id]='Rejected'
            data['STATUS'][id]='Rejected'
            rej_ids.append(id) 
    return top_ids,rej_ids,data


def make_dict(top_ids,data):
    top_dict={}
    for id in top_ids:
        top_dict[id]={}
    for id in top_ids:
        for title , values in data.items():
            for rowid , value in values.items():
                if id==rowid:
                    top_dict[id][title]=value
    return top_dict


def topView(request):
    csv_name='D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/MY-PARSED-DATA.csv'
    df_source = None
    data=[]
    if os.path.exists(csv_name):
        df_source = pd.DataFrame(pd.read_csv(csv_name,index_col=0))
    df_source=df_source.set_index('ROWID')
    # data=df_source.to_dict()
    ids,_,data=evaluate(df_source)
    data_dict=make_dict(ids,data)
    context={'data':data_dict,'labels':label_list}
    # context={'data_table':data_table,'top_ids':top_ids}
    return render(request,"home.html",context)

def allView(request):
    csv_name='D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/MY-PARSED-DATA.csv'
    df_source = None
    data=[]
    if os.path.exists(csv_name):
        df_source = pd.DataFrame(pd.read_csv(csv_name,index_col=0))
    df_source=df_source.set_index('ROWID')
    # data=df_source.to_dict()
    ids=[id for id in df_source.index]
    _,_,data=evaluate(df_source)
    data_dict=make_dict(ids,data)
    context={'data':data_dict,'labels':label_list}
    return render(request,"home.html",context)

def rejectedView(request):
    csv_name='D:/2mscCS/sem4/project/Resume Parser with NER/Parser/home/MY-PARSED-DATA.csv'
    df_source = None
    data=[]
    if os.path.exists(csv_name):
        df_source = pd.DataFrame(pd.read_csv(csv_name,index_col=0))
    df_source=df_source.set_index('ROWID')
    # data=df_source.to_dict()
    _,ids,data=evaluate(df_source)
    data_dict=make_dict(ids,data)
    context={'data':data_dict,'labels':label_list}
    return render(request,"home.html",context)