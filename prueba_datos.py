# -*- coding: utf-8 -*-
"""
Created on Thu May  9 08:33:42 2024

@author: gnper
"""

import pandas as pd
import requests

# datos = pd.read_csv("2022_pr.csv")

url = "https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/" + '2022' + "_PR/csv"
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
