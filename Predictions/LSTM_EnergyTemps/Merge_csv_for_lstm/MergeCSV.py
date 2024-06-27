'''
Imports
'''
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

plt.style.use('ggplot')
print('Imports done')

'''
Change the code to a value
'''
CODE_TO_VALUE = {
    3: 'HumitatRelMax',
    30: 'VelVent',
    31: 'DirVent',
    32: 'Temp',
    33: 'HumRel',
    35: 'Precip',
    36: 'Sol',
    40: 'TempMax',
    42: 'TempMin',
    44: 'HumRelMin',
    50: 'VelVentMax',
    51: 'DirVentMax',
    72: 'PrecipMax'
}

def ChangeCodi2Value(codi):
    '''
    Takes a code and returns the corresponding variable name using the dictionary CODE_TO_VALUE

    If the value doesn't exist in the dictionary it returns np.nan
    '''
    return CODE_TO_VALUE.get(codi, np.nan)

def group_data_by_date(df):
    '''
    Purpose: Converts and pivots the input dataframe (df) by grouping data by date (DateTime).
    '''
    column_names = ['DateTime', 'HumitatRelMax', 'VelVent', 'DirVent', 'Temp', 'HumRel', 'Precip', 'Sol', 'TempMax', 'TempMin', 'HumRelMin', 'PrecipMax']

    #Converts 'DATA_LECTURA' column to datetime format and assigns it to 'DateTime'.
    df['DateTime'] = pd.to_datetime(df['DATA_LECTURA'])

    #Pivots df on 'DateTime', CODI_VARIABLE, and VALOR_LECTURA to reshape the data.
    df_pivot = df.pivot(index='DateTime', columns='CODI_VARIABLE', values='VALOR_LECTURA').reset_index()

    #Renames columns to standard variable names (column_names).
    df_pivot.columns.name = None  # remove categories name
    df_pivot = df_pivot.reindex(columns=column_names)

    #Saves the pivoted dataframe to 'group_data_temps.csv'
    df_pivot.to_csv('group_data_temps.csv', index=False)
    return df_pivot

def arreglar_csv_temps(file):
    '''
    Purpose: Reads and preprocesses temperature data from CSV file (file).
    '''
    #Reads CSV file into data, parsing 'DATA_LECTURA' as dates and handling day-first format.
    data = pd.read_csv(file, parse_dates=['DATA_LECTURA'], dayfirst=True)

    #Maps CODI_VARIABLE codes to variable names using ChangeCodi2Value.
    data['CODI_VARIABLE'] = data['CODI_VARIABLE'].map(ChangeCodi2Value)

    #Drops rows where CODI_VARIABLE is NaN.
    data = data.dropna(subset=['CODI_VARIABLE'])

    #Filters out rows where CODI_VARIABLE is 'VelVentMax' or 'DirVentMax'. This two types have a lot of NaN values and don't seem useful.
    data = data[~data['CODI_VARIABLE'].isin(['VelVentMax', 'DirVentMax'])]

    #Calls group_data_by_date to pivot and process the dataframe & Returns the processed dataframe.
    return group_data_by_date(data)

def arreglar_csv_consum(file):
    '''
    Purpose: Reads and preprocesses energy consumption data from CSV file (file).
    '''
    #Reads CSV file into consum.
    consum = pd.read_csv(file)

    #Combines 'Date' and 'Hour' columns into a 'DateTime' column and parses it into datetime format.
    consum['DateTime'] = pd.to_datetime(consum['Date'] + ' ' + consum['Hour'], errors='coerce', infer_datetime_format=True)

    #Renames 'Q-Enginyeria-Total [kWh]' column to 'Energy' and drops 'Date' and 'Hour' columns.
    consum = consum.drop(columns=['Date', 'Hour']).rename(columns={'Q-Enginyeria-Total [kWh]': 'Energy'})

    # Drop rows where DateTime could not be parsed
    consum.dropna(subset=['DateTime'], inplace=True)
    print('Consum import done')

    return consum

def Unir_csv(consum_file, temps_file):
    '''
    Purpose: Integrates and merges preprocessed temperature and consumption data.
    '''
    #Calls arreglar_csv_consum and arreglar_csv_temps functions to preprocess consumption and temperature data.
    consum = arreglar_csv_consum(consum_file)
    temps = arreglar_csv_temps(temps_file)

    #Merges temps and consum dataframes on 'DateTime' using inner join (how='inner').
    merged_df = pd.merge(temps, consum, on='DateTime', how='inner')

    #Saves merged dataframe to 'Merged.csv'.
    merged_df.to_csv('Merged.csv', index=False)
    print('Everything done')

    return merged_df

'''
Main
'''
temps = 'Dades_meteorol_giques_de_la_XEMA_20240520.csv'
consum = 'Consum-energia-Q-2018-2023-horari.csv'
Tesco = Unir_csv(consum, temps)
print('Everything done')
