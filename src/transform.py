import pandas as pd
import numpy as np

def normalize_cols(df):
    return df.str.normalize('NFKD').str.replace("$","").str.replace("(","").str.replace(")","").str.replace('-','').str.replace(' ','_').str.lower().str.replace('.','')


def new_cases_deaths(df, ref_col='countryname', columns=['confirmed','deaths']):
    df.columns = normalize_cols(df.columns)

    df['date'] = pd.to_datetime(df['date'])
    df      = df.sort_values(by=[ref_col,'date'])
    
    for col in columns:    
        col_shift = f'{col}_shift'
        ref_shift = f'{ref_col}_shift'
        
        df[col_shift]   = df[col].shift(1)
        df[ref_shift] = df[ref_col].shift(1)
        
        # df[col_shift] = np.where(df[ref_shift]!=df[ref_col], 0 , df[col_shift])
        # df[f'new_{col}']       = df[col] - df[col_shift]
        
        df = df.drop(columns = [col_shift, ref_shift])
    
    return df


def transform_mytable(df):
    for col in ['confirmed','new_cases','deaths','new_deaths']:
        df[col] = pd.to_numeric(df[col])
        
    df_states         = df.sort_values(by=['date','confirmed'], ascending=False)
    df_states['city'] = df_states['state']
    df_states.head()

    mask   = (df_states['state']!='BRASIL') & (df_states['state']!='SP')
    not_sp = df_states[mask].groupby(by=['date'], as_index=False).sum()

    not_sp['state']  = 'BRASIL SEM SP'
    not_sp['city']   = 'BRASIL SEM SP'
    df_states        = pd.concat([df_states,not_sp[df_states.columns]],axis=0)
    
    return df_states