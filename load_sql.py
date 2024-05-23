import streamlit as st
import pymysql
import pandas as pd
import os
import json


myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "phonepe")

def agg_transaction(): 
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/aggregated/transaction/country/india/state/"
    ag = os.listdir(file_loc)

    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)
                for z in D['data']['transactionData']:
                    name = z['name']
                    count = z['paymentInstruments'][0]['count']
                    amount = z['paymentInstruments'][0]['amount']
                    sql = "insert into phonepe.agg_transaction values (%s,%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,name , count  ,amount )
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()


def agg_user(): 
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/aggregated/user/country/india/state/"
    ag = os.listdir(file_loc)
    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)
                users_by_device = D['data']['usersByDevice']
                if users_by_device is None:
                    continue 
                for device in D['data']['usersByDevice']:
                    brand_name = device['brand']
                    brand_count = device['count']
                    brand_percentage = device['percentage']
                    sql = "insert into phonepe.agg_user values (%s,%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,brand_name , brand_count  ,brand_percentage )
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

def top_transaction():
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/top/transaction/country/india/state/"
    ag = os.listdir(file_loc)
    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)

                for district in D['data']['districts']:
                    sql = "insert into phonepe.top_transaction_district values (%s,%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,district['entityName'],district['metric']['amount'],district['metric']['count'])
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

                for pincode in D['data']['pincodes']:
                    sql = "insert into phonepe.top_transaction_pincode values (%s,%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,pincode['entityName'],pincode['metric']['amount'],pincode['metric']['count'])
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

def top_user():
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/top/user/country/india/state/"
    ag = os.listdir(file_loc)
    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)

                for district in D['data']['districts']:
                    sql = "insert into phonepe.top_user_district values (%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,district['name'],district['registeredUsers'])
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

                for pincode in D['data']['pincodes']:
                    sql = "insert into phonepe.top_user_pincode values (%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,pincode['name'],pincode['registeredUsers'])
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

def map_transaction(): 
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/map/transaction/hover/country/india/state/"
    ag = os.listdir(file_loc)
    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)
                for district in D['data']['hoverDataList']:
                    sql = "insert into phonepe.map_transaction values (%s,%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,district['name'] , district['metric'][0]['amount']  ,district['metric'][0]['count'] )
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

def map_user(): 
    file_loc = "C:/Users/moham/Music/phonepe/data/pulse-master/data/map/user/hover/country/india/state/"
    ag = os.listdir(file_loc)
    for i in ag:
        p_i = file_loc+i+"/"
        ag_yr = os.listdir(p_i)
        for j in ag_yr:
            p_j = p_i + j + "/"
            agg_yr = os.listdir(p_j)
            for k in agg_yr:
                p_k = p_j +k
                Data = open(p_k,'r')
                D = json.load(Data)
                for district, info in D['data']['hoverData'].items():
                    sql = "insert into phonepe.map_user values (%s,%s,%s,%s,%s)"
                    values = (i.replace('-', ' ').title() , int(j) , int(k[0]) ,district , info['registeredUsers'] )
                    myconnection.cursor().execute(sql,values)
                    myconnection.commit()

agg_transaction()
agg_user()
map_transaction()
map_user()
top_transaction()
top_user()