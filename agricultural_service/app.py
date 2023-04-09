from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from joblib import load
import pathlib
# from pre_processing import *
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder,RobustScaler, LabelEncoder
import pandas as pd

app = FastAPI(title = 'Agricultural Produce Prediction')

init_float_col = ['min_rain', 'max_rain', 'avg_rain']
init_int_col = ['year_no', 'month_no']

## more general
class DataCastType_df(TransformerMixin):
  def __init__(self,float_cols=init_float_col,missing_indicator='?',int_cols=init_int_col):
    self.float_cols=float_cols
    self.int_cols=int_cols
    self.missing_indicator=missing_indicator
    
  def fit(self, X, y=None):
    self.cols=[col for col in X.columns if col not in self.float_cols+self.int_cols]
    return self

  def transform(self, X, y=None):
    X=X.replace(self.missing_indicator,np.nan)
    if self.float_cols:
      X[self.float_cols]=X[self.float_cols].astype(float)

    if self.int_cols:
      X[self.int_cols]=X[self.int_cols].astype(int)
   
    if self.cols:
      X[self.cols]=X[self.cols].astype('category')
    return X

class ModeNMedianFill(TransformerMixin):
  
  def fit(self, X, y = None):
    theDataMedian = X.median(numeric_only=True)
    theDataMode = X.mode().iloc[0]
    modeNmedian=theDataMode
    modeNmedian[theDataMedian.index.values.tolist()]=theDataMedian.values.tolist()
    self.treatment=modeNmedian
    return self

  def transform(self, X):
    return X.fillna(self.treatment)

  def fit_transform(self, X, y = None):
    return self.fit(X).transform(X)

class Outlier_truncation(TransformerMixin):
  def __init__(self,factor=1.5,numerical_cols=init_float_col):
    self.factor=factor
    self.numerical_cols=numerical_cols    
    
  def fit(self, X, y=None):
    Q1 = X[self.numerical_cols].quantile(0.25)
    Q3 = X[self.numerical_cols].quantile(0.75)
    IQR = Q3 - Q1
    self.lower_limit=Q1 - 1.5 * IQR
    self.upper_limit=Q3 + 1.5 * IQR
    return self

  def transform(self, X, y=None):
    for col in self.numerical_cols:
      X[col] = np.where(X[col] <self.lower_limit[col], self.lower_limit[col],X[col])
      X[col] = np.where(X[col] >self.upper_limit[col], self.upper_limit[col],X[col])
    return X



print(DataCastType_df)



model = load(pathlib.Path('models/argriculture-produce-prediction-v.1.0.joblib'))

class InputData(BaseModel):
    province_name:str='เชียงใหม่'
    min_rain:float=1 
    max_rain:float=3
    avg_rain:float=120
    year_no:int=267
    month_no:int=0
    plant:str='เงาะ'


class OutputData(BaseModel):
    produce_value:float=2345.67


@app.post('/predict', response_model = OutputData)
def score(data:InputData):
    # model_input = np.array([v for k,v in data.dict().items()]).reshape(1,-1)
    # result = model.predict(model_input)[:,-1]
    
    return {'produce_value':1234}