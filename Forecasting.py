# -*- coding: utf-8 -*-
"""Stage 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m9NwOO6kMuxzfmPzXHe3cGJTQmVRmDJu

Creating
Dictionary dict using
lat1 ,lon1 ,sst1,wind1,prec1

Importing required libraries and loading datasets

IMPORT DATA SETS
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt
# %matplotlib inline

# Import Statsmodels
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic

prec=nc.Dataset('/content/drive/MyDrive/Project/Phase 2/ Database/28 09 2018/Precipitation 28 09 2018/CMORPH_V1.0_ADJ_0.25deg-DLY_00Z_20180928.nc')
sst=nc.Dataset('/content/drive/MyDrive/Project/Phase 2/ Database/28 09 2018/SST 28 09 2018/oisst-avhrr-v02r01.20180928.nc')
wind=nc.Dataset('/content/drive/MyDrive/Project/Phase 2/ Database/28 09 2018/Wind 28 09 2018/uv20180928rt.nc')

"""Determining dimension
values existing in the dataset
"""

prec.variables.keys()
time = sst.variables['time'][:]
print(time)
print(wind.variables['time'][:])
print(prec.variables['time'][:])
print(prec.variables['time'][:])

lat=prec.variables['lat'][:]
lon=prec.variables['lon'][:]
sst1=sst.variables['sst'][:]
wind1=wind.variables['w'][:]
prec1=prec.variables['cmorph'][:]
time1 = prec.variables['time'][:]
time2 = sst.variables['time'][:]
time3 = wind.variables['time'][:]
zl2 = sst.variables['zlev'][:]
zl3 = wind.variables['zlev'][:]
len(time1)

t1 = prec.variables['time'][:]
t1

"""

*   Data Frame Construction
*   Loading Multidimensional data into list




"""

lat1=[]
lon1=[]
SST=[]
WIND=[]
PREC=[]


for i in range(len(lat)):
  for j in range(len(lon)):
    for t1 in range(len(time1)):
      for t2 in range(len(time2)):
        for t3 in range(len(time3)):
          for z2 in range(len(zl2)):
            for z3 in range(len(zl3)):
              
              if(prec1[t1,i,j]!='--' and wind1[t2,z2,i,j]!='--' and sst1[t3,z3,i,j] != '--'  ):
                 
                lat1.append(lat[i])
                lon1.append(lon[j])
                SST.append(sst1[t3,z3,i,j])
                WIND.append(wind1[0,0,i,j])
                PREC.append(prec1[0,i,j])

"""Creating
Dictionary dict using
lat1 ,lon1 ,sst1,wind1,prec1
"""

dict={'Lat':lat1,'Lon':lon1,'Wind':WIND ,'SST':SST,"Precipitation":PREC}
print(len(lat1))
print(len(lon1))
df=pd.DataFrame(dict)
df2=df
print(df2)

"""Calculate SST/WIND RATIO"""

df2[' ratio'] = df2['SST'] / df2['Wind']
df2

df3=df2
# df3=df3.drop(['Lat', 'Lon'], axis=1)

"""TIME SERIES REPRESENTATION OF WEATHER PARAMETERS"""

fig, axes = plt.subplots(nrows=4, ncols=2, dpi=120, figsize=(10,6))
for i, ax in enumerate(axes.flatten()):
    data = df3[df3.columns[i]]
    ax.plot(data, color='red', linewidth=1)
    # Decorations
    ax.set_title(df3.columns[i])
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines["top"].set_alpha(0)
    ax.tick_params(labelsize=4)

plt.tight_layout();

"""PLOT OF SUB DATABASE"""

df3.plot()

"""REMOVING INFINITE AND NaN values"""

df3 = df3[np.isfinite(df3).all(1)]
df3.replace([np.inf, -np.inf]).dropna(axis=1)
df3 = df3.dropna()

"""MODELLING PHASE

1. GRANGER CASUALITY TEST

TEST ON WIND AND SST
"""

from statsmodels.tsa.stattools import grangercausalitytests
data1 = df3[["Wind", "SST"]]
gc_res = grangercausalitytests(data1, 12)

"""TEST ON WIND AND PRECIPITATION"""

data1 = df3[["Wind", "Precipitation"]]
gc_res = grangercausalitytests(data1, 12)

"""TEST ON SST AND PRECIPITATION"""

data1 = df3[["SST", "Precipitation"]]
gc_res = grangercausalitytests(data1, 12)

"""2. COINTEGRATION TEST"""

from statsmodels.tsa.vector_ar.vecm import coint_johansen
def cointegration_test(df, alpha=0.05): 
    """Perform Johanson's Cointegration Test and Report Summary"""
    out = coint_johansen(df,-1,5)
    d = {'0.90':0, '0.95':1, '0.99':2}
    traces = out.lr1
    cvts = out.cvt[:, d[str(1-alpha)]]
    def adjust(val, length= 6): return str(val).ljust(length)

    # Summary
    print('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--'*20)
    for col, trace, cvt in zip(df.columns, traces, cvts):
        print(adjust(col), ':: ', adjust(round(trace,2), 9), ">", adjust(cvt, 8), ' =>  ' , trace > cvt)

cointegration_test(df3)

"""SPLITTING DATASET INTO TRAINING AND TESTING DATASET"""

df_train, df_test = df3[0:-4], df3[-4:]
print(df_train.shape)  # (119, 8)
print(df_test.shape)

"""STATIONARIZED DATA"""

#df_train = df_train.diff().dropna()
#df_test = df_test.diff().dropna()

"""APPLICATION OF VAR MODEL
1)FIND LAG ORDER 
"""

model = VAR(df_train)
for i in [1,2,3,4,5,6,7,8,9]:
    result = model.fit(i)
    print('Lag Order =', i)
    print('AIC : ', result.aic)
    print('BIC : ', result.bic)
    print('FPE : ', result.fpe)
    print('HQIC: ', result.hqic, '\n')

"""MATRIX COEFFICIENT"""

x = model.select_order(maxlags=12)
x.summary()

"""RUN MODEL ON LAG ORDER 12"""

model_fitted = model.fit(12)
model_fitted.summary()

lag_order = model_fitted.k_ar
print(lag_order)  
forecast_input = df_train.values[-lag_order:]
forecast_input

"""FORECASTING"""

fc = model_fitted.forecast(y=forecast_input, steps=4)
df_forecast = pd.DataFrame(fc, index=df3.index[-4:], columns=df3.columns + '_2d')
df_forecast

"""ACCURACY INFO"""

def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax =  np.mean(mins/maxs)             # minmax
    return({'mape':mape, 'me':me, 'mae': mae, 
            'mpe': mpe, 'rmse':rmse, 'corr':corr, 'minmax':minmax})

print('Forecast Accuracy of: Wind')
accuracy_prod = forecast_accuracy(df_forecast['Wind_2d'].values, df_test['Wind'])
for k, v in accuracy_prod.items():
    print(k, ': ', round(v,4))

print('\nForecast Accuracy of: SST')
accuracy_prod = forecast_accuracy(df_forecast['SST_2d'].values, df_test['SST'])
for k, v in accuracy_prod.items():
    print(k, ': ', round(v,4))
