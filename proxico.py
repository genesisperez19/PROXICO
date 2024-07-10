# -*- coding: utf-8 -*-
"""
Created on Thu May  9 08:32:06 2024

@author: gnper
"""

from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.io as pio
import plotly.express as px
import ssl
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import numpy as np
import requests
from geopy.geocoders import Nominatim
import plotly.colors
import dash_table
from googletrans import Translator


pio.renderers.default = "browser"
ssl._create_default_https_context = ssl._create_unverified_context

## Leer datos de centroides de municipios
centroides_df = pd.read_csv('https://cdat.uprh.edu/~genesis.perez20/proyecto3/Proyecto3/centroidesmunicipioslatlong.csv')
    
replacements = {
    'CATANO': 'CATAÑO',
    'PENUELAS': 'PEÑUELAS',
    'ANASCO': 'AÑASCO',
    'MAYAGUEZ': 'MAYAGÜEZ'
}
centroides_df['municipio'] = centroides_df['municipio'].str.upper().replace(replacements)
pueblos = list(centroides_df['municipio'])

## Funcion para convertir de gramos a libras
def convert_to_pounds(row):
    if row['UNIT OF MEASURE'] == 'Grams':
        row['5.1 - FUGITIVE AIR'] *= 0.00220462
        row['5.2 - STACK AIR'] *= 0.00220462
        row['5.3 - WATER'] *= 0.00220462
        row['5.4 - UNDERGROUND'] *= 0.00220462
        row['5.4.1 - UNDERGROUND CL I'] *= 0.00220462
        row['5.4.2 - UNDERGROUND C II-V'] *= 0.00220462
        row['5.5.1 - LANDFILLS'] *= 0.00220462
        row['5.5.1A - RCRA C LANDFILL'] *= 0.00220462
        row['5.5.1B - OTHER LANDFILLS'] *= 0.00220462
        row['5.5.2 - LAND TREATMENT'] *= 0.00220462
        row['5.5.3 - SURFACE IMPNDMNT'] *= 0.00220462
        row['5.5.3A - RCRA SURFACE IM'] *= 0.00220462
        row['5.5.3B - OTHER SURFACE I'] *= 0.00220462
        row['5.5.4 - OTHER DISPOSAL'] *= 0.00220462
        row['OFF-SITE RECYCLED TOTAL'] *= 0.00220462
        row['OFF-SITE ENERGY RECOVERY T'] *= 0.00220462
        row['OFF-SITE TREATED TOTAL'] *= 0.00220462
        row['6.2 - UNCLASSIFIED'] *= 0.00220462
        row['6.2 - TOTAL TRANSFER'] *= 0.00220462
        row['TOTAL RELEASES'] *= 0.00220462
        row['ON-SITE RELEASE TOTAL'] *= 0.00220462
        row['OFF-SITE RELEASE TOTAL'] *= 0.00220462
        row['UNIT OF MEASURE'] = 'Pounds'
    return row


## Función para traducir un texto usando Google Translate
translator = Translator()
def translate_text(text):
    try:
        if text.lower() == 'chemicals':
            return 'Químicos'
        translated_text = translator.translate(text, src='en', dest='es').text
    except Exception as e:
        translated_text = text  
    return translated_text

## Grafica vacia
def empty(pueblo, input_data):
    density_plot = go.Figure()
    density_plot.update_layout(
        title_text=f"No se encontraron datos de fábricas en {pueblo} para el {input_data}" ,
        title_x=0.5,
        title_y=0.5,
        title_font_size=20
    )
    
    density_plot.update_layout(height=550)  
    
    density_plot.update_xaxes(showticklabels=False)
    density_plot.update_yaxes(showticklabels=False)
    
    return density_plot

## Adquirir coordenadas del pueblo donde reside el usuario
def get_coordinates(address):
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Try to geocode the address
    location = geolocator.geocode(address)

    if location:
        # If location found, return latitude and longitude
        return location.latitude, location.longitude
    else:
        # If location not found, return None
        return None, None

## Grafica circular vacia
def empty_pie_chart_message(pueblo, input_data):
    # Create an empty pie chart layout with a message in the center
    empty_fig = go.Figure(go.Pie(labels=["No Data"], values=[100], hole=0.6))
    empty_fig.update_traces(marker=dict(colors=['rgba(255, 255, 255, 1)']))
    empty_fig.update_traces(textinfo='none', hoverinfo='none')
    empty_fig.update_layout(
        title= f"Porcentaje de Emisión de Sustancias Tóxicas en <b>{pueblo}</b> según su categoría",
        showlegend=False,
        annotations=[
            {
                "font": {"size": 20},
                "showarrow": False,
                "text": f"No se encontraron datos de fábricas en {pueblo} para el {input_data}",
                "x": 0.5,
                "y": 0.5
            }
        ]
    )
    return empty_fig

## Token de mapbox
token = 'pk.eyJ1IjoiZ2VuZXNpc3BlcmV6IiwiYSI6ImNsdHgycHo5eTAwZDgya2xxcG1tcml1MHEifQ.qcdoX4cPv47jiViWxPZO3w'
px.set_mapbox_access_token(token)


####################################################################################
#################################### APP ###########################################
####################################################################################


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    dbc.Container(fluid=True, style={'padding-top': '10px'}, children=[
        dbc.Row([
            dbc.Col(html.Div([
                    html.H1("PRóxico", style={'font-family': 'Times New Roman',
                                              'text-align': 'center',
                                              'color': '#ffffff',
                                              'font-size': '30px',
                                              'margin-top': '20px',
                                              'padding-left': '0px',
                                              'padding-right': '0px',
                                              'margin-left': '0px',
                                              'margin-right': '0px'}),
                    html.H1("Una aplicación para visualizar y analizar los datos del Toxics Release Inventory (TRI) Program para Puerto Rico",
                            style={'text-align': 'center',
                                   'color': '#ffffff',
                                   'font-size': '20px',
                                   'margin-top': '20px',
                                   'padding-left': '0px',
                                   'padding-right': '0px',
                                   'margin-left': '0px',
                                   'margin-right': '0px'}),
                    html.H1("Autor: Genesis N. Perez Gonzalez",
                            style={'text-align': 'center',
                                   'color': '#ffffff',
                                   'font-size': '16px',
                                   'margin-top': '10px',
                                   'padding-left': '0px',
                                   'padding-right': '0px',
                                   'margin-left': '0px',
                                   'margin-right': '0px'})
        ], style={'padding-left': '0px',
                  'padding-right': '0px',
                  'background-color': "#005ea2",
                  'color': '#ffffff', 
                  'margin-bottom': '20px',
                  'margin-left': '0px',
                  'margin-right': '0px', 
                  'padding-top':'3px',
                  'padding-bottom': '3px'}),
                )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                        html.H6("Año", style={'text-align': 'center', 'background-color': '#1a4480', 'padding': '8px','margin-bottom': '0px', 'color': '#ffffff'}),
                        dcc.Dropdown(
                            id='year',
                            options=[str(year) for year in range(1987, 2023)],
                            value='2022',
                            style={'padding': '0px', 'margin': 'auto', 'width': '300px', 'height': '35px', 'text-align': 'center'}
                            )
                        ], style={ 'background-color': '#1a4480', 'width': '100%', 'height': '76px'}), width={"size": 3, "offset": 0}
            ), 
            
            dbc.Col(
                html.Div([
                    html.H6('Dirección Física:', style={'text-align': 'center', 'background-color': '#1a4480', 'padding': '8px','margin-bottom': '0px', 'color': '#ffffff'}),
                    dcc.Input(id='direccion', 
                              type='text', 
                              placeholder="Avenida José E Aguiar Aramburu Carr. 908 KM 1.2.",
                              debounce=True,
                            style={'padding': '0px', 'margin-left': '30px', 'width': '300px', 'height': '35px', 'text-align': 'center','border-radius': '5px'}
                            )
                        ], style={ 'background-color': '#1a4480', 'width': '100%', 'height': '76px'}), width={"size": 3, "offset": 0}
            ), 
                          
            dbc.Col(
                html.Div([
                        html.H6("Pueblo", style={'text-align': 'center', 'background-color': '#1a4480', 'padding': '8px','margin-bottom': '0px', 'color': '#ffffff'}),
                        dcc.Dropdown(
                            id='pueblo',
                            options=pueblos,
                            value='HUMACAO',
                            style={'padding': '0px', 'margin': 'auto', 'width': '300px', 'height': '35px', 'text-align': 'center'}
                            )
                        ], style={ 'background-color': '#1a4480', 'width': '100%', 'height': '76px'}), width={"size": 3, "offset": 0}
            ), 
                          
            dbc.Col(
                html.Div([
                    html.H6('Zip Code:', style={'text-align': 'center', 'background-color': '#1a4480', 'padding': '8px','margin-bottom': '0px', 'color': '#ffffff'}),
                    dcc.Input(id='zip_code', 
                              type='text', 
                              placeholder="00792",
                              debounce=True,
                            style={'padding': '0px', 'margin-left': '30px', 'width': '300px', 'height': '35px', 'text-align': 'center','border-radius': '5px'}
                            )
                        ], style={'background-color': '#1a4480', 'width': '100%', 'height': '76px'}), width={"size": 3, "offset": 0}
            )
            
        ]),
        
        dbc.Row([
            dbc.Col(
                html.Div([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='bubble-graph'),
                        width={"size": 12}
                    )
                ])], style={'margin-top': '20px',
                            'border': '3px solid black',
                            'margin-bottom': '10px'}),
                width={"size": 6, "offset": 0}
            ),
            dbc.Col(
                html.Div([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='pie-chart'),
                        width={"size": 12}
                    )
                ])], style={'margin-top': '20px',
                            'border': '3px solid black',
                            'margin-left': '0px',
                            'padding-right': '0px',
                            'margin-bottom': '10px'}),
                width={"size": 6, "offset": 0}
            )
        ]),
                            
        dbc.Row([
            dbc.Col(html.Div([
                    html.H1(id='titulo_tabla', style={'font-size': '18px',
                                                          'margin-left': '10px',
                                                          'margin-top': '20px'})
        ], style={'height': '75px',
                  'border': '3px solid black',
                  'background-color': "#005ea2",
                  'color': '#ffffff',
                  'margin-bottom': '0px',
                  'margin-top': '15px',
                  'padding-top':'3px',
                  'text-align': 'center'}),
                )
        ]),
                            
        dbc.Row([
            dbc.Col(
                html.Div(id='table-container', children=[]),
                width={"size": 12, "offset": 0}
            )
        ]),
        
         dbc.Row([
            dbc.Col(html.Div([
                    html.H1(id='titulo_total', style={'font-size': '18px',
                                                          'margin-left': '10px',
                                                          'margin-top': '20px'})
        ], style={'height': '75px',
                  'border': '3px solid black',
                  'background-color': "#005ea2",
                  'color': '#ffffff',
                  'margin-bottom': '0px',
                  'margin-top': '15px',
                  'padding-top':'3px',
                  'text-align': 'center'}),
                )
        ]),
        
        dbc.Row([
            dbc.Col(
                html.Div([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='choropleth-graph'),
                        width={"size": 12}
                    )
                ])], style={'margin-top': '20px',
                            'border': '3px solid black',
                            'margin-left': '0px',
                            'padding-right': '0px',
                            'margin-bottom': '15px'}),
                width={"size": 6, "offset": 0}
            ),
            dbc.Col(
                html.Div([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='bar-graph'),
                        width={"size": 12}
                    )
                ])], style={'margin-top': '20px',
                            'border': '3px solid black',
                            'margin-bottom': '15px'
                            }),
                width={"size": 6, "offset": 0}
            )
        ])
        
    ])
])

 
   
########################################################################################################
##################################### Grafico de Burbujas ##############################################
########################################################################################################
    
@app.callback(
    Output('bubble-graph', 'figure'),
    [Input('year', 'value'),
     Input('direccion', 'value'),
     Input('pueblo', 'value'),
     Input('zip_code', 'value')]
)
def bubble_graph(input_data,direccion,pueblo,zipcode):
    if not input_data:
        input_data = '2022'
    
    if not direccion:
        direccion = "Avenida José E Aguiar Aramburu Carr. 908 KM 1.2."
    
    if not pueblo:
        pueblo = "HUMACAO"
    
    if not zipcode:
        zipcode = "00792"
    
    pueblo = pueblo.upper()
    
    municipio_data = centroides_df[centroides_df['municipio'] == pueblo.upper()]
    
    if municipio_data.empty:
        return empty(pueblo,input_data)
        
    # Verificar si existe data de el municipio
    if not municipio_data.empty:
        # Adquirir latitud y longitud del municipio
        y_lat = municipio_data['y_lat'].iloc[0]
        x_long = municipio_data['x_long'].iloc[0]
    
        # Adquirir data de TRI
        url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + input_data + "_PR/csv"
        response = requests.get(url)
    
        if response.status_code == 200:
            
            datos = pd.read_csv(url)
        
            # Modificar nombres de las columnas que tenian un numero al frente
            new_columns = {col: col.split('. ')[-1] for col in datos.columns}
            datos.rename(columns=new_columns, inplace=True)
            
            # Solo tener en COUNTY el nombre del municipio
            datos['COUNTY'] = datos['COUNTY'].apply(lambda x: x.rsplit(' ', 1)[0])
            
            replacements = {
                'CATANO': 'CATAÑO',
                'PENUELAS': 'PEÑUELAS',
                'ANASCO': 'AÑASCO',
                'MAYAGUEZ': 'MAYAGÜEZ'
            }
            
            datos['COUNTY'] = datos['COUNTY'].str.upper().replace(replacements)
            
            # Columnas de interes
            new_df = datos.loc[:, ['YEAR','TRIFD','FRS ID',
                                   'FACILITY NAME','STREET ADDRESS',
                                   'CITY','COUNTY','ST','ZIP','LATITUDE',
                                   'LONGITUDE','FEDERAL FACILITY',
                                   'INDUSTRY SECTOR','CHEMICAL','SRS ID',
                                   'CLASSIFICATION','METAL', 'CARCINOGEN',
                                   'UNIT OF MEASURE','5.1 - FUGITIVE AIR',
                                   '5.2 - STACK AIR','5.3 - WATER','5.4 - UNDERGROUND',
                                   '5.4.1 - UNDERGROUND CL I','5.4.2 - UNDERGROUND C II-V',
                                   '5.5.1 - LANDFILLS', '5.5.1A - RCRA C LANDFILL',
                                   '5.5.1B - OTHER LANDFILLS', '5.5.2 - LAND TREATMENT',
                                   '5.5.3 - SURFACE IMPNDMNT','5.5.3A - RCRA SURFACE IM',
                                   '5.5.3B - OTHER SURFACE I','5.5.4 - OTHER DISPOSAL',
                                   'ON-SITE RELEASE TOTAL','OFF-SITE RELEASE TOTAL',
                                   'OFF-SITE RECYCLED TOTAL','OFF-SITE ENERGY RECOVERY T',
                                   'OFF-SITE TREATED TOTAL','6.2 - UNCLASSIFIED',
                                   '6.2 - TOTAL TRANSFER','TOTAL RELEASES']]
      
            # Convertir de gramos a libras
            new_df = new_df.apply(convert_to_pounds, axis=1)
        
            df_release = new_df[['FACILITY NAME','COUNTY','LATITUDE',
                                   'LONGITUDE','FEDERAL FACILITY',
                                   'UNIT OF MEASURE','INDUSTRY SECTOR',
                                   'ON-SITE RELEASE TOTAL',
                                   'OFF-SITE RELEASE TOTAL']]
            
            # Traducir al español 
            df_release['FEDERAL FACILITY'] = df_release['FEDERAL FACILITY'].replace({'NO': 'No', 'YES': 'Si'})
            df_release['UNIT OF MEASURE'] = df_release['UNIT OF MEASURE'].replace({'Pounds': 'lbs.'})
            
            # Agrupar por fabricas
            df_release_new = df_release.groupby('FACILITY NAME').agg({
                'LATITUDE': 'first',
                'LONGITUDE': 'first',
                'FEDERAL FACILITY': 'first',
                'UNIT OF MEASURE': 'first',
                'INDUSTRY SECTOR': 'first',  
                'ON-SITE RELEASE TOTAL': 'sum',
                'OFF-SITE RELEASE TOTAL': 'sum'
            }).reset_index()
            
            # Traducir al español 
            df_release_new['INDUSTRY SECTOR'] = df_release_new['INDUSTRY SECTOR'].apply(translate_text)
            
            # Ordenar por total de emisiones
            df_release_new.sort_values(by='ON-SITE RELEASE TOTAL', ascending=False, inplace=True)
    
            df_release_new['log_ON-SITE RELEASE TOTAL'] = np.log(df_release_new['ON-SITE RELEASE TOTAL'] + 1)  # Adding 1 to avoid log(0)
            
            df_release_new['ON-SITE RELEASE TOTAL'] = df_release_new['ON-SITE RELEASE TOTAL'].apply(lambda x: "{:,.2f}".format(x))
            df_release_new['OFF-SITE RELEASE TOTAL'] = df_release_new['OFF-SITE RELEASE TOTAL'].apply(lambda x: "{:,.2f}".format(x))
    
            df_release_new['ON-SITE RELEASE TOTAL'] = df_release_new['ON-SITE RELEASE TOTAL'].astype(str) + ' ' + df_release_new['UNIT OF MEASURE']
            df_release_new['OFF-SITE RELEASE TOTAL'] = df_release_new['OFF-SITE RELEASE TOTAL'].astype(str) + ' ' + df_release_new['UNIT OF MEASURE']
        
    
            # Mapa de Burbujas
            mapa = px.scatter_mapbox(df_release_new, 
                                      lat="LATITUDE",
                                      lon="LONGITUDE",
                                      color='log_ON-SITE RELEASE TOTAL',
                                      size='log_ON-SITE RELEASE TOTAL',  
                                      color_continuous_scale='Reds',
                                      mapbox_style="light",
                                      zoom=11,  
                                      center={'lat': y_lat, 'lon': x_long},
                                      custom_data=['FACILITY NAME','FEDERAL FACILITY',
                                                   'INDUSTRY SECTOR','ON-SITE RELEASE TOTAL',
                                                   'OFF-SITE RELEASE TOTAL' ])
    
            hovertemplate = "<b>Fábrica:</b> %{customdata[0]}<br>" \
                            "<b>Agencia Federal:</b> %{customdata[1]}<br>" \
                            "<b>Sector Industrial:</b> %{customdata[2]}<br>" \
                            "<b>Total de Emisiones en el pueblo:</b> %{customdata[3]}<br>" \
                            "<b>Total de Emisiones fuera del pueblo:</b> %{customdata[4]}<br>" \
            
            mapa.update_traces(hovertemplate=hovertemplate)
            
            mapa.update_layout(height=550)   
            mapa.update_layout(title={
                'text': f"Fábricas en <b>{pueblo}</b> y su total de emisión de sustancias tóxicas para el {input_data}",
                'x':0.5, 
                'y':0.95   
            },coloraxis_showscale=False)
            
            mapa.add_shape(
            type="rect",
            x0=0, y0=0, x1=1, y1=1,
            xref='paper', yref='paper',
            line=dict(
                color="#4b607d",
                width=3,
            ),
            layer="above")
            
            return mapa
        
        else: 
            return empty(pueblo,input_data)



########################################################################################################
####################################### Grafico Circular ###############################################
########################################################################################################

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('year', 'value'),
     Input('direccion', 'value'),
     Input('pueblo', 'value'),
     Input('zip_code', 'value')]
)
def pie_chart(input_data, direccion, pueblo, zipcode):
    if not input_data:
        input_data = '2022'

    if not direccion:
        direccion = "Avenida José E Aguiar Aramburu Carr. 908 KM 1.2."

    if not pueblo:
        pueblo = "HUMACAO"

    if not zipcode:
        zipcode = "00792"

    pueblo = pueblo.upper()
    
    replacements = {
        'CATANO': 'CATAÑO',
        'PENUELAS': 'PEÑUELAS',
        'ANASCO': 'AÑASCO',
        'MAYAGUEZ': 'MAYAGÜEZ'
    }

    url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + input_data + "_PR/csv"
    response = requests.get(url)

    if response.status_code == 200:

        datos = pd.read_csv(url)

        # Modificar nombres de las columnas que tenian un numero al frente
        new_columns = {col: col.split('. ')[-1] for col in datos.columns}
        datos.rename(columns=new_columns, inplace=True)

        # Solo tener en COUNTY el nombre del municipio
        datos['COUNTY'] = datos['COUNTY'].apply(lambda x: x.rsplit(' ', 1)[0])
        datos.loc[:, 'COUNTY'] = datos['COUNTY'].str.upper().replace(replacements)


        # Solo tener datos del pueblo del usuario
        filtered_data = datos[datos['COUNTY'] == pueblo.upper()]
        
        # Convertir gramos a libras
        filtered_data = filtered_data.apply(convert_to_pounds, axis=1)
        
        
        if filtered_data.empty:
            return empty_pie_chart_message(pueblo, input_data)
        
        else:

            # Sumar categoria UNDERGROUND como un solo valor
            underground_total = (filtered_data['5.4 - UNDERGROUND'] + 
                                 filtered_data['5.4.1 - UNDERGROUND CL I'] + 
                                 filtered_data['5.4.2 - UNDERGROUND C II-V']).sum()
            
            # Sumar categoria LANDFILLS como un solo valor
            landfills_total = (filtered_data['5.5.1 - LANDFILLS'] + 
                               filtered_data['5.5.1A - RCRA C LANDFILL'] + 
                               filtered_data['5.5.1B - OTHER LANDFILLS']).sum()
            
            # Sumar categoriaSURFACE como un solo valor
            surface_total = (filtered_data['5.5.3 - SURFACE IMPNDMNT'] + 
                     filtered_data['5.5.3A - RCRA SURFACE IM'] + 
                     filtered_data['5.5.3B - OTHER SURFACE I']).sum()
            
     
            aggregated_data = filtered_data[['5.1 - FUGITIVE AIR', '5.2 - STACK AIR', '5.3 - WATER',
                                              '5.5.2 - LAND TREATMENT','5.5.4 - OTHER DISPOSAL']]

            aggregated_data.columns = [col.split(" - ")[-1] for col in aggregated_data.columns]
    
            aggregated_data['UNDERGROUND'] = round(underground_total,2)
            aggregated_data['LANDFILLS'] = round(landfills_total,2)
            aggregated_data['SURFACE'] = round(surface_total,2)
            
            # Traducir al español
            column_name_mapping = {
                                    'FUGITIVE AIR': 'Aire fugitivo',
                                    'STACK AIR': 'Aire de chimenea',
                                    'WATER': 'Cuerpos de Agua',
                                    'LAND TREATMENT': 'Tratamiento de tierra',
                                    'OTHER DISPOSAL': 'Otro método de disposición',
                                    'UNDERGROUND': 'Disposición Soterrada',
                                    'LANDFILLS': 'Vertederos',
                                    'SURFACE': 'Superficies'
                                }
 
            aggregated_data = aggregated_data.rename(columns=column_name_mapping)
                
            # Total por cada categoria
            aggregated_data = round(aggregated_data.sum(),2)
                        
            color_palette = plotly.colors.sequential.matter
        
            fig = go.Figure(data=[go.Pie(labels=aggregated_data.index, 
                                         values=aggregated_data.values, 
                                         marker=dict(colors=color_palette))])
                    
            fig.update_traces(textposition='inside', 
                  textinfo='percent+label', 
                  hoverinfo='label+value',  # Muestra la etiqueta y el valor en el hover
                  hovertemplate='%{label}: %{value} lbs.<extra></extra>')  # Agrega la unidad "lbs."

            
    
            fig.update_layout(height=550) 
            fig.update_layout(title={
                'text': f"Porcentaje de Emisión de Sustancias Tóxicas en <b>{pueblo}</b> según su categoría",
                'x':0.5, 
                'y':0.95   
            })
            
            
            fig.update_layout(
                margin=dict(l=150, r=50, t=70, b=50))
            
            return fig
    
    else: 
        return empty_pie_chart_message(pueblo, input_data)

# ########################################################################################################
# ############################# Tabla de las fabricas en el pueblo #######################################
# ########################################################################################################

@app.callback(
    Output('titulo_tabla', 'children'),
    [Input('year', 'value'),
     Input('direccion', 'value'),
     Input('pueblo', 'value'),
     Input('zip_code', 'value')]
)
def titulo_tabla(input_data, direccion, pueblo, zipcode):
    if not input_data:
        input_data = '2022'
    if not pueblo:
        pueblo = "HUMACAO"
    
    pueblo = pueblo.upper()
    
    return f"Tabla de Emisión de Sustancias Tóxicas de las Fábricas en {pueblo} para el {input_data}"


@app.callback(
    Output('table-container', 'children'),
    [Input('year', 'value'),
     Input('direccion', 'value'),
     Input('pueblo', 'value'),
     Input('zip_code', 'value')]
)
def tabla(input_data, direccion, pueblo, zipcode):
    if not input_data:
        input_data = '2022'
    
    if not direccion:
        direccion = "Avenida José E Aguiar Aramburu Carr. 908 KM 1.2."
    
    if pueblo is None:
        pueblo = "HUMACAO"
    else:
        pueblo = pueblo.upper()

    if not zipcode:
        zipcode = "00792"
    
    replacements = {
        'CATANO': 'CATAÑO',
        'PENUELAS': 'PEÑUELAS',
        'ANASCO': 'AÑASCO',
        'MAYAGUEZ': 'MAYAGÜEZ'
    }
    
    url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + input_data + "_PR/csv"
    response = requests.get(url)

    if response.status_code == 200:
        datos = pd.read_csv(url)
    
        # Modificar nombres de las columnas que tenian un numero al frente
        new_columns = {col: col.split('. ')[-1] for col in datos.columns}
        datos.rename(columns=new_columns, inplace=True)
    
        # Solo tener en COUNTY el nombre del municipio
        datos['COUNTY'] = datos['COUNTY'].apply(lambda x: x.rsplit(' ', 1)[0])
        datos.loc[:, 'COUNTY'] = datos['COUNTY'].str.upper().replace(replacements)
    
        # Tener datos del pueblo del usuario
        filtered_data = datos[datos['COUNTY'] == pueblo.upper()]
        
        # Conversiones y traducciones
        filtered_data = filtered_data.apply(convert_to_pounds, axis=1)
        filtered_data['FEDERAL FACILITY'] = filtered_data['FEDERAL FACILITY'].replace({'NO': 'No', 'YES': 'Si'})
        filtered_data['UNIT OF MEASURE'] = filtered_data['UNIT OF MEASURE'].replace({'Pounds': 'lbs.'})
        filtered_data['METAL'] = filtered_data['METAL'].replace({'NO': 'No', 'YES': 'Si'})
        filtered_data['CARCINOGEN'] = filtered_data['CARCINOGEN'].replace({'NO': 'No', 'YES': 'Si'})
        
        filtered_data.sort_values(by='ON-SITE RELEASE TOTAL', ascending=False, inplace=True)
        
        filtered_data['ON-SITE RELEASE TOTAL'] = filtered_data['ON-SITE RELEASE TOTAL'].apply(lambda x: "{:,.2f}".format(x))
        filtered_data['ON-SITE RELEASE TOTAL'] = filtered_data['ON-SITE RELEASE TOTAL'].astype(str) + ' ' + filtered_data['UNIT OF MEASURE']
        
        if filtered_data.empty:
            return [html.P(f"No se encontraron datos de fábricas en {pueblo} para el {input_data}", className="text-center")]
        else:
            translated_columns = {
                                    'INDUSTRY SECTOR': 'SECTOR INDUSTRIAL',
                                    'CHEMICAL': 'QUÍMICO',
                                    'METAL': 'METAL',
                                    'CARCINOGEN': 'CARCINÓGENO',
                                    'ON-SITE RELEASE TOTAL': 'TOTAL DE EMISIÓN',
                                    'FACILITY NAME': 'NOMBRE DE LA INSTALACIÓN',
                                    'CLASSIFICATION': 'CLASIFICACIÓN'
                                }
            filtered_data.rename(columns=translated_columns, inplace=True)
    
            new_df = filtered_data.loc[:, ['NOMBRE DE LA INSTALACIÓN', 'SECTOR INDUSTRIAL', 'QUÍMICO',
                                       'CLASIFICACIÓN', 'METAL', 'CARCINÓGENO', 'TOTAL DE EMISIÓN']]
            
            new_df['SECTOR INDUSTRIAL'] = new_df['SECTOR INDUSTRIAL'].apply(translate_text)
            new_df['QUÍMICO'] = new_df['QUÍMICO'].apply(translate_text)
    
            # Tabla
            table = dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in new_df.columns],
                data=new_df.to_dict('records'),
                style_table={'overflowX': 'scroll', 'border': '3px solid black'},
                style_cell={'textAlign': 'left'},
                style_header={
                    'border': '3px solid black',
                    'border-collapse': 'collapse',
                    'border-spacing': '0'
                },
            )
    
            return [table]

    else:
        return [html.P("Error extrayendo la data")]


# ########################################################################################################
# ###################################### Datos nivel isla ################################################
# ########################################################################################################


@app.callback(
    Output('titulo_total', 'children'),
    [Input('year', 'value'),
     Input('direccion', 'value'),
     Input('pueblo', 'value'),
     Input('zip_code', 'value')]
)
def titulo_total(input_data, direccion, pueblo, zipcode):
    if not input_data:
        input_data = '2022'
    if not pueblo:
        pueblo = "HUMACAO"
    
    pueblo = pueblo.upper()
    
    return "Emisión de Sustancias Tóxicas a nivel isla"



# ########################################################################################################
# ############################################ Choropleth ################################################
# ########################################################################################################


@app.callback(
    Output('choropleth-graph', 'figure'),
    [Input('year', 'value')]
)
def choropleth_graph(input_data):
    if not input_data:
        input_data = '2022'
    
    url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + input_data + "_PR/csv"
    response = requests.get(url)

    if response.status_code == 200:
        datos = pd.read_csv(url)
    
        # Modificar nombres de las columnas que tenian un numero al frente
        new_columns = {col: col.split('. ')[-1] for col in datos.columns}
        datos.rename(columns=new_columns, inplace=True)
        
        # Solo tener en COUNTY el nombre del municipio
        datos['COUNTY'] = datos['COUNTY'].apply(lambda x: x.rsplit(' ', 1)[0])
        
        replacements = {
            'CATANO': 'CATAÑO',
            'PENUELAS': 'PEÑUELAS',
            'ANASCO': 'AÑASCO',
            'MAYAGUEZ': 'MAYAGÜEZ'
        }
        
        datos['COUNTY'] = datos['COUNTY'].str.upper().replace(replacements)

        new_df = datos.loc[:, ['YEAR','TRIFD','FRS ID',
                               'FACILITY NAME','STREET ADDRESS',
                               'CITY','COUNTY','ST','ZIP','LATITUDE',
                               'LONGITUDE','FEDERAL FACILITY',
                               'INDUSTRY SECTOR','CHEMICAL','SRS ID',
                               'CLASSIFICATION','METAL', 'CARCINOGEN',
                               'UNIT OF MEASURE','5.1 - FUGITIVE AIR',
                               '5.2 - STACK AIR','5.3 - WATER','5.4 - UNDERGROUND',
                               '5.4.1 - UNDERGROUND CL I','5.4.2 - UNDERGROUND C II-V',
                               '5.5.1 - LANDFILLS', '5.5.1A - RCRA C LANDFILL',
                               '5.5.1B - OTHER LANDFILLS', '5.5.2 - LAND TREATMENT',
                               '5.5.3 - SURFACE IMPNDMNT','5.5.3A - RCRA SURFACE IM',
                               '5.5.3B - OTHER SURFACE I','5.5.4 - OTHER DISPOSAL',
                               'ON-SITE RELEASE TOTAL','OFF-SITE RELEASE TOTAL',
                               'OFF-SITE RECYCLED TOTAL','OFF-SITE ENERGY RECOVERY T',
                               'OFF-SITE TREATED TOTAL','6.2 - UNCLASSIFIED',
                               '6.2 - TOTAL TRANSFER','TOTAL RELEASES']]

        new_df = new_df.apply(convert_to_pounds, axis=1)
        new_df['FEDERAL FACILITY'] = new_df['FEDERAL FACILITY'].replace({'NO': 'No', 'YES': 'Si'})
        new_df['UNIT OF MEASURE'] = new_df['UNIT OF MEASURE'].replace({'Pounds': 'lbs.'})


        df_frecuencia = new_df[['COUNTY', 'ON-SITE RELEASE TOTAL']].copy()
        df_frecuencia.columns = ['municipio', 'frecuencia']
        df_frecuencia = df_frecuencia.groupby('municipio')['frecuencia'].sum().reset_index()
        df_frecuencia.sort_values(by='frecuencia', ascending=False, inplace=True)
        
        # Abrir geojson con poligonos de los municipios
        url_geojson = 'https://github.com/commonwealth-of-puerto-rico/crime-spotter/raw/master/public/data/municipalities.geojson'
        with urlopen(url_geojson) as response:
            municipalities = json.load(response)
            
            
        rep = str.maketrans("ÁÉÍÓÚ","AEIOU")
        municipalities_names_geojson = [muni['properties']['NAME'].upper() for muni in municipalities['features']]
        municipalities_names_geojson = [name.translate(rep) for name in municipalities_names_geojson]
        
        # AAñadir municipios faltantes del GeoJSON al df_frecuencia con frecuencia 0
        missing_municipalities = set(municipalities_names_geojson) - set(df_frecuencia['municipio'])
        missing_municipalities_df = pd.DataFrame({'municipio': list(missing_municipalities), 'frecuencia': 0})
        df_frecuencia = pd.concat([df_frecuencia, missing_municipalities_df], ignore_index=True)
        
        df_frecuencia.sort_values(by='frecuencia', ascending=False, inplace=True)
        
        df_frecuencia['log_ON-SITE RELEASE TOTAL'] = np.log(df_frecuencia['frecuencia'] + 1)
                
        
        for muni in municipalities['features']:
            muni['properties']['NAME'] = muni['properties']['NAME'].upper().translate(rep)

        choropleth = px.choropleth(df_frecuencia, geojson=municipalities, locations="municipio", color='log_ON-SITE RELEASE TOTAL',
                            featureidkey="properties.NAME",
                            color_continuous_scale="Reds",
                            custom_data=['frecuencia'])
        
        choropleth.update_geos(fitbounds="locations", visible=False)
        
        choropleth.update_traces(hovertemplate="<b>Municipio:</b> %{location}<br><b>Total de Emisión:</b> %{customdata[0]:,.2f} lbs.")
        
        choropleth.update_layout(height=550)  
        choropleth.update_layout(title={
            'text': "Total de emisiones de sustancias tóxicas por municipio",
            'x':0.5, 
            'y':0.95   
        },coloraxis_showscale=False)
        
        choropleth.add_shape(
        type="rect",
        x0=0, y0=0, x1=1, y1=1,
        xref='paper', yref='paper',
        line=dict(
            color="#4b607d",
            width=3,
        ),
        layer="above")
        
        
        return choropleth



# ########################################################################################################
# ############################################### Bar Graph ##############################################
# ########################################################################################################
    
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('year', 'value')]
)

def bar_graph(input_data):
    if not input_data:
        input_data = '2022'
    
    url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + input_data + "_PR/csv"
    response = requests.get(url)

    if response.status_code == 200:
        datos = pd.read_csv(url)
    
        # Modificar nombres de las columnas que tenian un numero al frente
        new_columns = {col: col.split('. ')[-1] for col in datos.columns}
        datos.rename(columns=new_columns, inplace=True)
        
        # Solo tener en COUNTY el nombre del municipio
        datos.loc[:, 'COUNTY'] = datos['COUNTY'].apply(lambda x: x.rsplit(' ', 1)[0])
        
        replacements = {
            'CATANO': 'CATAÑO',
            'PENUELAS': 'PEÑUELAS',
            'ANASCO': 'AÑASCO',
            'MAYAGUEZ': 'MAYAGÜEZ'
        }
        
        datos['COUNTY'] = datos['COUNTY'].str.upper().replace(replacements)
        
        new_df = datos.loc[:, ['YEAR','TRIFD','FRS ID',
                               'FACILITY NAME','STREET ADDRESS',
                               'CITY','COUNTY','ST','ZIP','LATITUDE',
                               'LONGITUDE','FEDERAL FACILITY',
                               'INDUSTRY SECTOR','CHEMICAL','SRS ID',
                               'CLASSIFICATION','METAL', 'CARCINOGEN',
                               'UNIT OF MEASURE','5.1 - FUGITIVE AIR',
                               '5.2 - STACK AIR','5.3 - WATER','5.4 - UNDERGROUND',
                               '5.4.1 - UNDERGROUND CL I','5.4.2 - UNDERGROUND C II-V',
                               '5.5.1 - LANDFILLS', '5.5.1A - RCRA C LANDFILL',
                               '5.5.1B - OTHER LANDFILLS', '5.5.2 - LAND TREATMENT',
                               '5.5.3 - SURFACE IMPNDMNT','5.5.3A - RCRA SURFACE IM',
                               '5.5.3B - OTHER SURFACE I','5.5.4 - OTHER DISPOSAL',
                               'ON-SITE RELEASE TOTAL','OFF-SITE RELEASE TOTAL',
                               'OFF-SITE RECYCLED TOTAL','OFF-SITE ENERGY RECOVERY T',
                               'OFF-SITE TREATED TOTAL','6.2 - UNCLASSIFIED',
                               '6.2 - TOTAL TRANSFER','TOTAL RELEASES']]

        new_df = new_df.apply(convert_to_pounds, axis=1)
        new_df['FEDERAL FACILITY'] = new_df['FEDERAL FACILITY'].replace({'NO': 'No', 'YES': 'Si'})
        new_df['UNIT OF MEASURE'] = new_df['UNIT OF MEASURE'].replace({'Pounds': 'lbs.'})

        df_frecuencia = new_df[['FACILITY NAME', 'COUNTY', 'ON-SITE RELEASE TOTAL','FEDERAL FACILITY',
                               'INDUSTRY SECTOR']]
        df_frecuencia = df_frecuencia.groupby('FACILITY NAME')['ON-SITE RELEASE TOTAL'].sum().reset_index()
        df_frecuencia['log_ON-SITE RELEASE TOTAL'] = np.log(df_frecuencia['ON-SITE RELEASE TOTAL'] + 1)
        
        counties = []
        federal = []
        sector = []
        for facility_name in df_frecuencia['FACILITY NAME']:
            county = new_df.loc[new_df['FACILITY NAME'] == facility_name, 'COUNTY'].iloc[0]
            counties.append(county)
            
            federal_facility = new_df.loc[new_df['FACILITY NAME'] == facility_name, 'FEDERAL FACILITY'].iloc[0]
            federal.append(federal_facility)
            
            industry_sector = new_df.loc[new_df['FACILITY NAME'] == facility_name, 'INDUSTRY SECTOR'].iloc[0]
            sector.append(industry_sector)
            
        df_frecuencia['COUNTY'] = counties
        df_frecuencia['FEDERAL FACILITY'] = federal
        df_frecuencia['INDUSTRY SECTOR'] = sector
        
        df_frecuencia.sort_values(by='ON-SITE RELEASE TOTAL', ascending=False, inplace=True)
        
        top5 = df_frecuencia[0:5]
        top5['INDUSTRY SECTOR'] = top5['INDUSTRY SECTOR'].apply(translate_text)
        
        fig = px.bar(top5,
              x="FACILITY NAME",  
              y="ON-SITE RELEASE TOTAL", 
              color="log_ON-SITE RELEASE TOTAL",
              orientation="v", 
              color_continuous_scale='Reds',
              custom_data=['FACILITY NAME','COUNTY','ON-SITE RELEASE TOTAL','FEDERAL FACILITY',
                               'INDUSTRY SECTOR'],
              color_continuous_midpoint=None) 

        fig.update_traces(hovertemplate="<b>Fábrica:</b> %{customdata[0]}<br><b>Municipio:</b> %{customdata[1]}<br><b>Total de Emisión:</b> %{customdata[2]:,.2f} lbs.<br><b>Agencia Federal:</b> %{customdata[3]}<br><b>Sector Industrial:</b> %{customdata[4]}")
        fig.update_layout(height=550)  
        fig.update_layout(title={
            'text': f"Fábricas con mayor cantidad de emisión de sustancias tóxicas para el {input_data}",
            'x':0.5, 
            'y':0.95   
        })
        
        fig.add_shape(
            type="rect",
            x0=0, y0=0, x1=1, y1=1,
            xref='paper', yref='paper',
            line=dict(
                color="black",
                width=1,
            ),
            layer="above")
        
        fig.update_layout(
            margin=dict(l=150, r=50, t=70, b=50),
            coloraxis_colorbar=None  # This line removes the colorbar legend
        )
        
        fig.update_traces(showlegend=False)
        fig.update(layout_coloraxis_showscale=False)
        
        return fig
    


if __name__ == '__main__':
    app.run_server(debug=True)

