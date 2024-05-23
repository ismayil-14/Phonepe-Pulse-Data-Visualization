import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import pymysql
import requests
import json
from streamlit_option_menu import option_menu

myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "phonepe")

st.set_page_config(layout="wide")
st.title("PhonePe Project")




tab0,tab1,tab2= st.tabs(["Home","Transactions ", "Users "])

with tab0:
    st.header("Home Page")


    st.write("## Overview")
    st.write("The PhonePe Pulse Dashboard Project is designed to transform complex data into insightful, interactive, and visually appealing visualizations. Our goal is to leverage the extensive data available in the PhonePe Pulse GitHub repository to create a user-friendly dashboard that provides valuable insights and information.")
    st.write("We start by efficiently fetching and cloning data from the GitHub repository. Using Python and libraries like Pandas, we clean and preprocess the data to make it suitable for analysis and visualization. The cleaned data is then stored in a MySQL database for efficient retrieval and management.")
    st.write("With Streamlit and Plotly, we build an interactive dashboard that showcases the data on a geo map and provides multiple dropdown options for users to explore various facts and figures. The dashboard dynamically fetches data from the MySQL database, ensuring real-time updates.")
    st.write("Our dashboard offers an intuitive interface, making it easy for users to navigate and explore the data. Accessible from any web browser, it provides meaningful insights and information, making it a powerful tool for data analysis and decision-making.")


with tab1:
    st.header("Map Analysis")

    col1, col2 = st.columns(2)

    with col1:
        year = st.selectbox(
            'Year',
            (2018,2019,2020,2021,2022,2023,"Overall")
        )
    with col2:
        quarter = st.selectbox(
            'Quarter',
            (1,2,3,4,"Overall")
        )
    if year == "Overall" and quarter == "Overall":
        query = f"""Select * from agg_transaction """
    elif year == "Overall":
        query = f"""Select * from agg_transaction where quarter = {quarter}  """
    elif quarter == "Overall":
        query = f"""Select * from agg_transaction where year = {year} """
    else:
        query = f"""Select * from agg_transaction where Year = {year} && Quarter = {quarter}"""
    dataFrame = pd.read_sql_query(query,myconnection)


    col3,col4 = st.columns(2)

    with col3:
        st.title("Transaction Amount")
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
        states_name[0] = "Andaman & Nicobar Islands"

        fig_india_1= px.choropleth(dataFrame, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(0, 1000000000),
                                hover_name= "State", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col4:
        st.title("Aggergated Transaction Values")

        st.write("")
        st.write("")
        st.write("")

        query1 = """Select * from agg_transaction """
        dataFrame1= pd.read_sql_query(query1,myconnection)
        
        st.write("#### Total Transactions : ", dataFrame1[["Transaction_amount"]].sum().values[0])

        st.write("#### Total Transaction Count : ", dataFrame1[["Transaction_count"]].sum().values[0])

        st.write("#### Average Transaction values : " , round(dataFrame1[["Transaction_amount"]].sum().values[0]/dataFrame1[["Transaction_count"]].sum().values[0],4))
        st.write("_____________________________________________")
        category =  dataFrame1.groupby('Transaction_type')['Transaction_amount'].sum()

        st.write('#### Overall Recharge & bill payments', category['Recharge & bill payments'])
        st.write('#### Overall Peer-to-peer payments',category['Peer-to-peer payments'] )
        st.write('#### Overall Merchant payments', category['Merchant payments'] )
        st.write('#### Overall Financial Services' , category['Financial Services'])
        st.write('#### Overall Others', category['Others'])

    st.write('_________________________________________________________________________________________________________________________')
    
    col5, col6 = st.columns(2)

    with col5:
        st.title("Categories")

        category1 =  dataFrame.groupby('Transaction_type')['Transaction_amount'].sum()

        st.write('### Recharge & bill payments', category1['Recharge & bill payments'])
        st.write('### Peer-to-peer payments',category1['Peer-to-peer payments'] )
        st.write('### Merchant payments', category1['Merchant payments'] )
        st.write('### Financial Services' , category1['Financial Services'])
        st.write('### Others', category1['Others'])

    with col6:
        fig = go.Figure(data=[go.Pie(labels=category.index, values=category)])

        # Display the Pie chart in Streamlit
        st.plotly_chart(fig)

    st.write('_________________________________________________________________________________________________________________________')


    col61, col62 = st.columns(2)
    with col61:
        query1a = f"""select State, sum(Amount) as "Total Amount" from map_transaction group by State """
        dataFrame1a = pd.read_sql_query(query1a,myconnection)

        fig = px.line(dataFrame1a, x='State', y='Total Amount', title='Overall Total Amount by State')
        st.plotly_chart(fig)
    with col62:

        if year != "Overall" and quarter != "Overall":
            query1b = f"""select State, sum(Amount) as "Total Amount" from map_transaction where Year = {year} and Quarter = {quarter} group by State"""
            dataFrame1b = pd.read_sql_query(query1b,myconnection)

            fig = px.line(dataFrame1b, x='State', y='Total Amount', title=f'         Total Amount by State Year wise - {year} in Quarter- {quarter}')
            st.plotly_chart(fig)



    st.write('_________________________________________________________________________________________________________________________')
    st.title("State")
    state = st.selectbox(
        '',
        tuple(states_name)
    )

    if year == "Overall" and quarter == "Overall":
        query2 = f"""Select * from agg_transaction where State = '{state}' """
    elif year == "Overall":
        query2 = f"""Select * from agg_transaction where State = '{state}' and Quarter = {quarter}"""
    elif quarter == "Overall":
        query2 = f"""Select * from agg_transaction where State = '{state}' and Year = {year} """
    else:
        query2 = f"""Select * from agg_transaction where State = '{state}' and Year = {year} && Quarter = {quarter}"""

    dataFrame2= pd.read_sql_query(query2,myconnection)
    col7, col8 = st.columns([6,4])
    with col8:
        category2 =  dataFrame2.groupby('Transaction_type')['Transaction_amount'].sum()
        st.write("")
        st.write("")
        st.write("")
        st.write('### Recharge & bill payments', category2['Recharge & bill payments'])
        st.write('### Peer-to-peer payments',category2['Peer-to-peer payments'] )
        st.write('### Merchant payments', category2['Merchant payments'] )
        st.write('### Financial Services' , category2['Financial Services'])
        st.write('### Others', category2['Others'])

    with col7:
        fig = go.Figure(data=[go.Pie(labels=category2.index, values=category2)])

        # Display the Pie chart in Streamlit
        st.plotly_chart(fig)
    
    st.write('_________________________________________________________________________________________________________________________')


    option = st.radio("View Data for:", ("State", "Overall"))
    col9,col10,col11 = st.columns([3,4,3])


    with col9:
        st.header("Total Amount by State")

        if year == "Overall" and quarter == "Overall":
            query3 = """SELECT State as "State", SUM(Amount) as "Total Amount" FROM map_transaction GROUP BY State ORDER BY SUM(Amount) DESC LIMIT 10;"""
        elif year == "Overall":
            query3 = f"""SELECT State as "State", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Quarter = {quarter} GROUP BY State ORDER BY SUM(Amount) DESC LIMIT 10;"""
        elif quarter == "Overall":
            query3 = f"""SELECT State as "State", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} GROUP BY State ORDER BY SUM(Amount) DESC LIMIT 10;"""
        else:
            query3 = f"""SELECT State as "State", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} AND Quarter = {quarter} GROUP BY State ORDER BY SUM(Amount) DESC LIMIT 10;"""

        dataFrame3= pd.read_sql_query(query3,myconnection)
        st.table(dataFrame3)

    with col10:
        st.header("Total Amount by District")

        if option == "State":
            if year == "Overall" and quarter == "Overall":
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE State = '{state}' GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            elif year == "Overall":
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Quarter = {quarter} AND State = '{state}' GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            elif quarter == "Overall":
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} AND State = '{state}' GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            else:
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} AND Quarter = {quarter} AND State = '{state}' GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
        else:  # option == "Overall"
            if year == "Overall" and quarter == "Overall":
                query4 = """SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            elif year == "Overall":
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Quarter = {quarter} GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            elif quarter == "Overall":
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""
            else:
                query4 = f"""SELECT District_name as "District", SUM(Amount) as "Total Amount" FROM map_transaction WHERE Year = {year} AND Quarter = {quarter} GROUP BY District_name ORDER BY SUM(Amount) DESC LIMIT 10;"""

        dataFrame4= pd.read_sql_query(query4,myconnection)
        st.table(dataFrame4)

    with col11:
        st.header("Total Amount by Pincode")

        if option == "State":
            if year == "Overall" and quarter == "Overall":
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE State = '{state}' GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            elif year == "Overall":
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Quarter = {quarter} AND State = '{state}' GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            elif quarter == "Overall":
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Year = {year} AND State = '{state}' GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            else:
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Year = {year} AND Quarter = {quarter} AND State = '{state}' GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
        else:  # option == "Overall"
            if year == "Overall" and quarter == "Overall":
                query5 = """SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            elif year == "Overall":
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Quarter = {quarter} GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            elif quarter == "Overall":
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Year = {year} GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""
            else:
                query5 = f"""SELECT Pincode as "Pincode", SUM(Pincode_amount) as "Total Amount" FROM top_transaction_pincode WHERE Year = {year} AND Quarter = {quarter} GROUP BY Pincode ORDER BY SUM(Pincode_amount) DESC LIMIT 10;"""

        dataFrame5= pd.read_sql_query(query5,myconnection)
        st.table(dataFrame5)
    



with tab2:
    st.header("Map Analysis")

    Acol1, Acol2 = st.columns(2)

    with Acol1:
        Ayear = st.selectbox(
            'Year',
            (2023,2022,2021,2020,2019,2018)
        )
    with Acol2:
        Aquarter = st.selectbox(
            'Quarter',
            (4,3,2,1)
        )

    Aquery = f"""select State, Year, Quarter,sum(District_users) as "User Count" from map_user where Year = {Ayear} && Quarter = {Aquarter} group by State, Year, Quarter;"""
    AdataFrame = pd.read_sql_query(Aquery,myconnection)


    Acol3,Acol4 = st.columns(2)

    with Acol3:
        st.title("User Count")
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
        states_name[0] = "Andaman & Nicobar Islands"


        fig_india_1= px.choropleth(AdataFrame, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                color= "User Count", color_continuous_scale= "Rainbow",
                                range_color=(AdataFrame['User Count'].min(), AdataFrame['User Count'].min()),
                                hover_name= "State", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with Acol4:
        for i in range(1,16):

            st.write("")
        Aquery1 = f"""select sum(District_users) from map_user where Year <={Ayear};"""
        AdataFrame1= pd.read_sql_query(Aquery1,myconnection)

        st.write(f"## Total User Count Till {Ayear} is {AdataFrame1.iloc[0,0]}")

        Aquery2 = f"""select sum(District_users) from map_user where Year = {Ayear} group by Year;"""
        AdataFrame2= pd.read_sql_query(Aquery2,myconnection)

        st.write("")
        st.write("")
        st.write("")

        st.write(f"## Total User Count in {Ayear} is {AdataFrame2.iloc[0,0]}")
    
            

    st.title("Mobile Brand Usage")

    Aquery3 = """select brand,sum(brand_count) as "Brand Count"  from agg_user group by brand ;"""
    AdataFrame3= pd.read_sql_query(Aquery3,myconnection)

    st.write("_____________________________________________")

    fig = px.bar(AdataFrame3, x='brand', y='Brand Count', title=f'         Total User count by Mobile brand')
    
    fig.update_layout(
width=1400,
margin=dict(l=20, r=20, t=50, b=20),
title=dict(x=0.5)  # Center the title
)
    st.plotly_chart(fig)
    st.write('_________________________________________________________________________________________________________________________')
    
    Astate = st.selectbox(
        '',
        tuple(states_name[::-1])
    )        
    Acol5,Acol6,Acol7 = st.columns([3,4,3])


    with Acol5:
        st.header("Total User by State")
        query3 = f"""select State as "State" , sum(District_users) as "User Count" from map_user where Year = {Ayear} and Quarter = {Aquarter} group by State order by sum(District_users) desc limit 10;"""
        dataFrame3= pd.read_sql_query(query3,myconnection)
        st.table(dataFrame3)

    with Acol6:
        st.header("Total User by District")
        query4 = f"""select District_name as "District" , sum(District_users) as "User Count" from top_user_district where Year = {Ayear} and Quarter = {Aquarter} and State = '{Astate}' group by District_name order by sum("User Count") desc limit 10;"""
        dataFrame4= pd.read_sql_query(query4,myconnection)
        st.table(dataFrame4)

    with Acol7:
        st.header("Total User by Pincode")
        query5 = f"""select Pincode as "Pincode" , sum(Pincode_users) as "Total Amount" from top_user_pincode where Year = {Ayear} and Quarter = {Aquarter} and State = '{Astate}' group by Pincode order by sum("User Count") desc limit 10;"""
        dataFrame5= pd.read_sql_query(query5,myconnection)
        st.table(dataFrame5)