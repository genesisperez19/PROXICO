# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:07:54 2024

Autor: Genesis N. Perez Gonzalez 
Curso: COMP 4010-001
Proyecto Final

"""
PRóxico (proxico.py) es una aplicación diseñada para analizar y visualizar los datos 
del Programa de Inventario de Emisiones Tóxicas (TRI) para Puerto Rico (PR). 

## Funcionalidades

El objetivo principal de PRóxico es permitir al usuario explorar los 
datos de emisiones tóxicas en Puerto Rico de una manera visual e interactiva. 
Las principales características incluyen:

- Selección de Año: El usuario puede seleccionar el año para el cual desea 
                    visualizar los datos.
                    
- Ubicación Física: Se requiere la dirección física del usuario (calle, pueblo,
                    zipcode) para enfocar la visualización en su área de 
                    residencia.
                    
- Visualización de Datos: La aplicación presenta gráficos y tablas que muestran
                          información relevante sobre las emisiones tóxicas en
                          Puerto Rico.

## Componentes

Mapa de Burbujas

- Muestra las fábricas por municipios, centrándose en el pueblo de residencia 
  del usuario.
- Indica el total de libras de emisión de sustancias tóxicas en el pueblo de 
  residencia y fuera de él.
- Identifica si la fábrica es de jurisdicción federal y a qué sector industrial
  pertenece.
- Los puntos y colores corresponden al total de emisiones en el pueblo de 
  residencia.

Gráfica Circular

- Presenta el porcentaje total de emisión de sustancias tóxicas por categoría 
  de emisión en el pueblo de residencia del usuario.

Tabla

- Detalla información sobre las fábricas en el pueblo de residencia del usuario.
- Indica el tipo de químico liberado, si es metal o no metal, si es carcinógeno 
  o no, y su clasificación:
                           TRI = General EPCRA Section 313 Chemical
                           PBT = Persistent Bioaccumulative and Toxic
                           DIOXIN = Dioxin or Dioxin-like compound.
- Muestra la cantidad emitida de dicho químico.

Mapa Coroplético

- Muestra el total de emisiones de sustancias tóxicas en cada municipio de 
  Puerto Rico.

Gráfico de Barras

- Presenta las 5 fábricas a nivel de isla con mayor total de emisión de 
  sustancias tóxicas.

## Mejoras Futuras

- Localización Exacta: Considerar la dirección exacta del usuario para obtener 
  la longitud y latitud, permitiendo una visualización más específica de las 
  fábricas cercanas.
  
- Impacto en la Salud: Evaluar cómo las emisiones de sustancias tóxicas 
  podrían afectar la salud de residentes cercanos, considerando su proximidad
  a las fábricas.

- Contaminación de Cuerpos de Agua: Analizar si hay cuerpos de agua cercanos 
  que puedan estar siendo contaminados por las sustancias liberadas.

## Notas Adicionales

Actualmente, la aplicación se enfoca en proporcionar información a nivel de 
isla y sobre las fábricas que liberan sustancias tóxicas en el pueblo de 
residencia del usuario. Se espera continuar mejorando y ampliando sus 
funcionalidades en futuras versiones.

