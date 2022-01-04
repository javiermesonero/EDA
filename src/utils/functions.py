import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def configuracion():
    st.set_page_config(
     page_title="Cargatron",
     page_icon=":electric_plug:",
     layout="wide")
def cargaDatos(csvPath):
    return pd.read_csv(csvPath)
def dividirDatos(df):
    df_city=df[df['hotel']=='City Hotel']
    df_resort=df[df['hotel']== 'Resort Hotel'] 
    return df_city,df_resort
    

def menu(df,df_city,df_resort):
    panel_pos=st.selectbox('Página',['1','2','3'])  

    if panel_pos=='1':
        panel1(df,df_city,df_resort)
    elif panel_pos=='2':
        panel2()
    elif panel_pos=='3':
        panel3()
    




def panel1 (df,df_city,df_resort):
    fig=plt.figure()
    sns.barplot(x=df_city['arrival_date_year'],y=df_city['adults'],color='green',estimator=sum)
    sns.barplot(x=df_city['arrival_date_year'],y=df_city['babies'],color='blue',estimator=sum)
    sns.barplot(x=df_city['arrival_date_year'],y=df_city['children'],color='red',estimator=sum)
    plt.legend()
    st.pyplot(fig)

def panel2 ():
    st.title('hola')   

def panel3 ():
    st.title('adios')       