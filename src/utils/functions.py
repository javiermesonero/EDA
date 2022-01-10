import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.express as px

def configuracion():
    st.set_page_config(
     page_title="Cargatron",
     page_icon=":electric_plug:",
     layout="wide")
def cargaDatosLimpios(csvPath):
    df= pd.read_csv(csvPath)
    df=df[df['is_canceled']==0]#nos interesa la gente que viene al hotel y no cencela
    mask=(df['adults']>0)|(df['children']>0)|(df['babies']>0) #comprobamos que no es una reserva vacia
    df=df[mask]
    mask= ((df['customer_type']=='Transient')|(df['customer_type']=='Transient-Party'))
    df=df[mask] #nos quedamos con las reservas normales fuera de grupos y contratos
    df["meal"].replace({"Undefined": "SC", }, inplace=True)
    return df
def dividirDatos(df):
    df_city=df[df['hotel']=='City Hotel']
    df_resort=df[df['hotel']== 'Resort Hotel'] 
    return df_city,df_resort
    

def menu(df,df_city,df_resort):
    panel_pos=st.selectbox('Página',['0','1','2','3','4','5','6','7','8','9'])  
    if panel_pos=='0':
        panel0(df)
    elif panel_pos=='1':
        panel1(df,df_city,df_resort)
    elif panel_pos=='2':
        panel2(df,df_city,df_resort)
    elif panel_pos=='3':
        panel3(df,df_city,df_resort)
    elif panel_pos=='4':
        panel4(df,df_city,df_resort)  
    elif panel_pos=='5':
        panel5(df,df_city,df_resort) 
    elif panel_pos=='6':
        panel6(df,df_city,df_resort)     
    elif panel_pos=='7':
        panel7(df,df_city,df_resort) 
    elif panel_pos=='8':
        panel8(df,df_city,df_resort) 
    elif panel_pos=='9':
        panel9(df,df_city,df_resort) 







def panel0(df):
    st.write('''hablamos de los datos, por que fuera cancelados y grupos y contratos,
     que datos usamos para mostrar, 
    tambien contamos que columnas nos van a interesar y porque''') 
    st.dataframe(df.head())

def mostrarGraficaBarras(df,tiempo,scale):
    trace1 = go.Bar(x = df.groupby(tiempo).sum()['adults'].index ,
                        y = df.groupby(tiempo).sum()['adults'] )
    trace2 = go.Bar(x = df.groupby(tiempo).sum()['babies'].index,
                        y = df.groupby(tiempo).sum()['babies'] )
    trace3 = go.Bar(x = df.groupby(tiempo).sum()['children'].index ,
                        y = df.groupby(tiempo).sum()['children']  )
    data = [trace1,trace2,trace3]

    layout = go.Layout(barmode='group')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    st.plotly_chart(fig)    


def panel1 (df,df_city,df_resort):
    a,b,c=st.columns(3)
    with b: 
        button_mes=st.button('mes')      
    with a:
        button_ano=st.button('año')
    with c:
        button_semana=st.button('semana')     
    
    code='arrival_date_year'
    scale=80000
    if button_ano:
        code='arrival_date_year'
        scale=80000
    elif button_mes:
        code='arrival_date_month'
        scale=20000
    elif button_semana:
        code='arrival_date_week_number'
        scale=5000


    with st.expander('Gráfica de clientes totales',expanded=True):
        a,b,c=st.columns(3)
        with b:
            mostrarGraficaBarras(df,code,scale)         
        with a:
            st.write(' ')  
        with c:
            st.write(' ')      

    c1,c2=st.columns(2)

    with c1:
    # create trace1 
        mostrarGraficaBarras(df_city,code,scale)
        st.markdown('Gráfica de clientes de ciudad')

    with c2:
    # create trace1 
        mostrarGraficaBarras(df_resort,code,scale)
        st.write('      Gráfica de clientes de resort')



def mostrarGraficaFamilia(df,scale=0.3):
    
    trace1 = go.Bar(x = df.groupby('adults').mean()['children'].index ,
                        y = df.groupby('adults').mean()['children'] )
    trace2 = go.Bar(x = df.groupby('adults').mean()['babies'].index,
                        y = df.groupby('adults').mean()['babies'] )
    data = [trace1,trace2]

    layout = go.Layout(barmode='group')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    fig.update_xaxes(range=[-1,5])
    st.plotly_chart(fig) 


def panel2 (df,df_city,df_resort):
    st.title('Familias')
    a,b,c=st.columns(3)
    with b:
        mostrarGraficaFamilia(df,scale=2.5)        
    with a:
        st.write(' ')  
    with c:
        st.write(' ') 


    
    c1,c2=st.columns(2)
    with c1:
        mostrarGraficaFamilia(df_city)
        st.write('city')
    with c2:
        mostrarGraficaFamilia(df_resort) 
        st.write('resort')

def mostrarTreeMap(df):
    df.groupby(['reserved_room_type','assigned_room_type']).size()
    fig = px.treemap(df,
                 path=['reserved_room_type', 'assigned_room_type'])
    fig.show()   
    st.plotly_chart(fig) 

def panel3 (df,df_city,df_resort):

    a,b,c=st.columns(3)
    with b:
        mostrarTreeMap(df)      
    with a:
        st.write(' ')  
    with c:
        st.write(' ') 

    c1,c2=st.columns(2)
    with c1:
        mostrarTreeMap(df_city)
        st.write('city')
    with c2:
        mostrarTreeMap(df_resort)
        st.write('resort')    


def mostrarStackCharSum(df,scale=7500):
    trace1 = go.Bar(x = df.groupby('arrival_date_week_number').sum()['stays_in_weekend_nights'].index ,
                    y = df.groupby('arrival_date_week_number').sum()['stays_in_weekend_nights'] )
    trace2 = go.Bar(x = df.groupby('arrival_date_week_number').sum()['stays_in_week_nights'].index,
                    y = df.groupby('arrival_date_week_number').sum()['stays_in_week_nights'] )
    data = [trace1,trace2]

    layout = go.Layout(barmode='stack')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    iplot(fig)
    st.plotly_chart(fig)

def mostrarStackCharMean(df,scale=5.5):
    trace1 = go.Bar(x = df.groupby('arrival_date_week_number').mean()['stays_in_weekend_nights'].index ,
                    y = df.groupby('arrival_date_week_number').mean()['stays_in_weekend_nights'] )
    trace2 = go.Bar(x = df.groupby('arrival_date_week_number').mean()['stays_in_week_nights'].index,
                    y = df.groupby('arrival_date_week_number').mean()['stays_in_week_nights'] )
    data = [trace1,trace2]

    layout = go.Layout(barmode='stack')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    iplot(fig)
    st.plotly_chart(fig)


def panel4(df,df_city,df_resort):
    st.write('hola')
    a1,b1=st.columns(2)
    with a1: 
        button_sum=st.button('sum')      
    with b1:
        button_mean=st.button('mean')

    if button_sum:
        a,b,c=st.columns(3)
        with b:
            mostrarStackCharSum(df)      
        with a:
            st.write(' ')  
        with c:
            st.write(' ') 


        c1,c2=st.columns(2)
        with c1:
            mostrarStackCharSum(df_city)
            st.write('city')
        with c2:
            mostrarStackCharSum(df_resort)
            st.write('resort')  
    elif button_mean:
        a,b,c=st.columns(3)
        with b:
            mostrarStackCharMean(df)      
        with a:
            st.write(' ')  
        with c:
            st.write(' ') 


        c1,c2=st.columns(2)
        with c1:
            mostrarStackCharMean(df_city)
            st.write('city')
        with c2:
            mostrarStackCharMean(df_resort)
            st.write('resort')

def mostrarMapa(df):
    fig = go.Figure(data=go.Choropleth(
    locations=df.groupby('country').size().index, # Spatial coordinates
    z = df.groupby('country').size().values# Data to be color-coded
    , colorscale = 'Viridis'))

    fig.show()
    st.plotly_chart(fig)

def panel5(df,df_city,df_resort):
    st.write('5')
    a,b,c=st.columns(3)
    with a: 
        st.button('total')      
    with b:
        button_city=st.button('city')
    with c:
        button_resort=st.button('resort') 
    
    if button_city:
        mostrarMapa(df_city)   
    elif button_resort:
        mostrarMapa(df_resort)
    else :
        mostrarMapa(df)



def mostrarPie(df):
    fig = {
    "data": [
    {
      "values": df.groupby('required_car_parking_spaces').size(),
      "labels": (df.required_car_parking_spaces.unique()),
      "name": "Number Of Students Rates",
      "hoverinfo":"label+percent+name",
      "type": "pie"
    },],
    "layout": {
        'legend_title_text':'Number of Cars'
        }
    }

    iplot(fig)
    st.plotly_chart(fig)

def panel6(df,df_city,df_resort):
    st.write('6')
    a,b,c=st.columns(3)
    with a: 
        st.write(' ')  
    with b:
        mostrarPie(df)
    with c:
        st.write(' ')


    c1,c2=st.columns(2)
    with c1:
        mostrarPie(df_city)
        st.write('city')
    with c2:
        mostrarPie(df_resort)
        st.write('resort')  



def mostrarPieMeal(df):
    fig = {
    "data": [
    {
      "values": df.groupby('meal').size(),
      "labels": (df.meal.unique()),
      "name": "Number Of Students Rates",
      "hoverinfo":"label+percent+name",
      "type": "pie"
    },],
    "layout": {
        'legend_title_text':'Number of meal'
    }
    }
    iplot(fig)
    st.plotly_chart(fig)
def mostrarPieMeal2(df,order):
    fig = go.Figure(data=[go.Pie(labels=order,
                             values=df.groupby('meal').size())])
    fig.update_layout(legend_title="Legend Title")                         
    fig.show()
    st.plotly_chart(fig)

def panel7(df,df_city,df_resort):
    '''st.write(df.groupby('meal').size())
    st.write(df_city.groupby('meal').size())
    st.write(df_resort.groupby('meal').size())
    st.write(df.meal.unique())
    st.write(df_city.meal.unique())
    st.write(df_resort.meal.unique())'''
    order=(df.meal.unique())
    

    a,b,c=st.columns(3)
    with a: 
        st.write(' ')  
    with b:
        mostrarPieMeal2(df,order)
    with c:
        st.write(' ')


    c1,c2=st.columns(2)
    with c1:
        mostrarPieMeal2(df_city,order)
        st.write('city')
    with c2:
        mostrarPieMeal2(df_resort,order)
        st.write('resort') 



def panel8(df,df_city,df_resort):
     st.write('8')

def panel9(df,df_city,df_resort):
    st.write('9')
