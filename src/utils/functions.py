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
     page_title="EDA Hoteles",
     page_icon=":hotel:",
     layout="wide")
def cargaDatosLimpios(csvPath):
    df= pd.read_csv(csvPath)
    df=df[df['is_canceled']==0]#nos interesa la gente que viene al hotel y no cencela
    mask=(df['adults']>0)|(df['children']>0)|(df['babies']>0) #comprobamos que no es una reserva vacia
    df=df[mask]
    mask= ((df['customer_type']=='Transient')|(df['customer_type']=='Transient-Party'))
    df=df[mask] #nos quedamos con las reservas normales fuera de grupos y contratos
    df["meal"].replace({"Undefined": "SC", }, inplace=True) #las reservas con regimen sin definir las convertimos en reservas sin regimen
    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']) 
    #convertimos la fecha de entrada para facilitar su uso en las graficas
    
    return df
def dividirDatos(df):
    #divide los datos en dos dataframe segun el hotel al que le pertenece
    df_city=df[df['hotel']=='City Hotel']
    df_resort=df[df['hotel']== 'Resort Hotel'] 
    return df_city,df_resort
    

def menu(df,df_city,df_resort):
    #funcion principal de visualizacion del programa
    #es un select box, para cada elección el el selecbox hay una funcion panel asignada
    #cada panel es un conjunto de graficas distintas, como paginas de una presentación
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
    st.write('''EDA: hoteles en Portugal''') 

    c1,c2=st.columns(2)
    with c1:
        st.image('../img/hotel_ciudad.jpg')
    with c2:
        st.image('../img/hotel_campo.jpg')

    st.dataframe(df.head())

def mostrarGraficaBarras(df,tiempo,scale):
    #muestra una grafica de barras con tres medidas, suma de adultos,ninos y bebes en un determinado tiempo: ano, mes, semana
    #la escala nos permite eligir el maximo en la grafica d el eje Y


    trace1 = go.Bar(x = df.groupby(tiempo).sum()['adults'].index ,
                        y = df.groupby(tiempo).sum()['adults'],name='adultos' )
    trace2 = go.Bar(x = df.groupby(tiempo).sum()['babies'].index,
                        y = df.groupby(tiempo).sum()['babies'],name='bebés' )
    trace3 = go.Bar(x = df.groupby(tiempo).sum()['children'].index ,
                        y = df.groupby(tiempo).sum()['children'] ,name='niños' )
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
    #muestra una grafica de barras con dos valores, la media de ninos y bebes por el numero de adultos
    #scale nos permite establecer el maximo de la grafica del eje Y
    trace1 = go.Bar(x = df.groupby('adults').mean()['children'].index ,
                        y = df.groupby('adults').mean()['children'],name='niños' )
    trace2 = go.Bar(x = df.groupby('adults').mean()['babies'].index,
                        y = df.groupby('adults').mean()['babies'],name='bebés' )
    data = [trace1,trace2]

    layout = go.Layout(barmode='group')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    fig.update_xaxes(range=[-1,5])
    st.plotly_chart(fig) 

def mostrarGraficaFamiliaDistribucion(df,scale=33000):
    #mostrar una grafica de barras con datos de la distribucion de cuantos grupos de adultos van solos o con ninos segun el numero de adultos
    #scale nos permite establecer el maximo de la grafica del eje Y


    mask1=    (df['children']>0) | (df['babies']>0)
    mask2=    (df['children']==0) | (df['babies']==0)

    trace1 = go.Bar(x = df[mask1].groupby('adults').size().index ,
                            y = df[mask1].groupby('adults').size() ,name='Reservas con al menos un niño o bebé')
    trace2 = go.Bar(x = df[mask2].groupby('adults').size().index,
                            y = df[mask2].groupby('adults').size(),name='Reservas sin ningún niño ni bebé')
    data = [trace2,trace1]

    layout = go.Layout(barmode='group')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    iplot(fig)    
    st.plotly_chart(fig) 

def mostrarPieFamilias(df):
    #muestra una grafica de tarta con la distribucion de que porcentaje de reservas tienen ninos frente a las que no
    mask1=    (df['children']>0) | (df['babies']>0)
    mask2=    (df['children']==0) | (df['babies']==0)
    labels = [' No Familias','Familias']
    values = [df[mask2].groupby('adults').size().sum(),df[mask1].groupby('adults').size().sum()]

    fig = {
    "data": [
    {
      "values": values,
      "labels": labels,
      "name": "Number Of Students Rates",
      "hoverinfo":"label+percent+name",
      "type": "pie"
    },],
    "layout": {
        'legend_title_text':' '
        }
    }

    iplot(fig)
    st.plotly_chart(fig)

def panel2 (df,df_city,df_resort):
    #que porcentaje de num adultos va solo y cual lleva por lo menos un niño
    with st.expander(' ',expanded=True):
        a,b,c=st.columns(3)
        with b:
            #mostrarGraficaFamilia(df,scale=2.5)        
            mostrarGraficaFamiliaDistribucion(df,scale=55000)
        with a:
            st.write(' ')  
        with c:
            st.write(' ') 


    
    c1,c2=st.columns(2)
    with c1:
        #mostrarGraficaFamilia(df_city)
        mostrarGraficaFamiliaDistribucion(df_city)
        mostrarPieFamilias(df_city)
        st.write('city')
    with c2:
        #mostrarGraficaFamilia(df_resort) 
        mostrarGraficaFamiliaDistribucion(df_resort)
        mostrarPieFamilias(df_resort)
        st.write('resort')

def mostrarTreeMap(df):
    #muestra un treemap con informacion de que habiatacion se ha solicitado frente al tipo de habitacion que se ha asignado
    df.groupby(['reserved_room_type','assigned_room_type']).size()
    fig = px.treemap(df,
                 path=['reserved_room_type', 'assigned_room_type'])
    fig.show()   
    st.plotly_chart(fig) 

def panel3 (df,df_city,df_resort):
    with st.expander(' ',expanded=True):
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
    #muestra una grafica de barras stacked con informacion de la suma de estancia de dias entresemna y fin de semana
    #scale nos permite establecer el maximo de la grafica del eje Y
    trace1 = go.Bar(x = df.groupby('arrival_date_week_number').sum()['stays_in_weekend_nights'].index ,
                    y = df.groupby('arrival_date_week_number').sum()['stays_in_weekend_nights'],name='Días de estancia fin de semana' )
    trace2 = go.Bar(x = df.groupby('arrival_date_week_number').sum()['stays_in_week_nights'].index,
                    y = df.groupby('arrival_date_week_number').sum()['stays_in_week_nights'] ,name='Días de estancia Lunes-Viernes')
    data = [trace1,trace2]

    layout = go.Layout(barmode='stack')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    iplot(fig)
    st.plotly_chart(fig)

def mostrarStackCharMean(df,scale=5.5):
    #muestra una grafica de barras stacked con informacion de la media de estancia de dias entresemna y fin de semana
    #scale nos permite establecer el maximo de la grafica del eje Y
    trace1 = go.Bar(x = df.groupby('arrival_date_week_number').mean()['stays_in_weekend_nights'].index ,
                    y = df.groupby('arrival_date_week_number').mean()['stays_in_weekend_nights'] ,name='Días de estancia Lunes-Viernes')
    trace2 = go.Bar(x = df.groupby('arrival_date_week_number').mean()['stays_in_week_nights'].index,
                    y = df.groupby('arrival_date_week_number').mean()['stays_in_week_nights'] ,name='Días de estancia fin de semana')
    data = [trace1,trace2]

    layout = go.Layout(barmode='stack')


    fig = go.Figure(data = data, layout = layout)
    fig.update_yaxes(range=[0,scale])
    iplot(fig)
    st.plotly_chart(fig)


def panel4(df,df_city,df_resort):
    a1,b1=st.columns(2)
    with a1: 
        st.button('sum')      
    with b1:
        button_mean=st.button('mean')

    if button_mean:
        with st.expander(' ',expanded=True):
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
    else :
        with st.expander(' ',expanded=True):
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

def mostrarMapa(df):
    #muestra un mapa con la distribucion de densidad de gente por paises
    fig = go.Figure(data=go.Choropleth(
    locations=df.groupby('country').size().index, # Spatial coordinates
    z = df.groupby('country').size().values# Data to be color-coded
    , colorscale = 'Viridis'))

    fig.show()
    st.plotly_chart(fig)

def panel5(df,df_city,df_resort):
   
    a,b,c=st.columns(3)
    with a: 
        st.button('total')      
    with b:
        button_city=st.button('city')
    with c:
        button_resort=st.button('resort') 
    
    if button_city:
        a1,b1,c1=st.columns(3)
        with b1:
            mostrarMapa(df_city)       
        with a1:
            st.write(' ')  
        with c1:
            st.write(' ') 
          
    elif button_resort:
        a1,b1,c1=st.columns(3)
        with b1:
            mostrarMapa(df_resort)       
        with a1:
            st.write(' ')  
        with c1:
            st.write(' ')
        
    else :
        a1,b1,c1=st.columns(3)
        with b1:
            mostrarMapa(df)       
        with a1:
            st.write(' ')  
        with c1:
            st.write(' ')



def mostrarPie(df):
    #muestra un grafico de tarta con informacion de distribucion de densidad de la cantidad de coches en el parking
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
    with st.expander(' ',expanded=True):
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
    #muestra un grafico de pie con la distribucion de densidad del tipo de regimen
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
    #muestra un grafico de pie con la distribucion de densidad del tipo de regimen
    #order te permite utilizarun orden por defecto 
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
    
    with st.expander(' ',expanded=True):
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
    c1,c2=st.columns(2)
    with c1:
        st.title('Hotel de Ciudad')
        st.subheader('- Mayor volumen de clientes, más constantes a lo largo del año')
        st.subheader('- La procedencia de los clientes es más diversa y el volumen de clientes extranjeros es similar al nacional')
        st.subheader('- El uso del parking es residual')
    with c2:
        st.title('Hotel Resort') 
        st.subheader('- Menor volumen de cliente con subidas en verano y puentes vacacionales')
        st.subheader('- La procedencia de los clientes es poco diversa y principalmente nacional')
        st.subheader('- El uso del parking es bajo pero necesario para algunos clientes')

def panel9(df,df_city,df_resort):
    
    a,b,c = st.columns([1,2,1])
    with a:
        st.write('')
    with b:
        st.title('Conclusiones para ambos hoteles')
        st.subheader('- Ampliar el numero de habitaciones tipo A en ambos hoteles')
        st.subheader('- Intentar captar mayor número de clientes para pensiones superiores a B & B')

    with c:
        st.write(' ')


