import streamlit as st
import pandas as pd
import functions as ft

csvPath='../data/hotel_bookings.csv'
ft.configuracion()
df=ft.cargaDatos(csvPath)
df_city,df_resort=ft.dividirDatos(df)
ft.menu(df,df_city,df_resort)
