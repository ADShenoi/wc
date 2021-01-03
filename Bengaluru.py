import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import streamlit as st

df = pd.read_csv('Bengaluru.csv')
df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)
enc = OrdinalEncoder()
df[['Wind']] = enc.fit_transform(df[['Wind']])
def changesymbol(x):
    symbol=['F','%','mph','in']
    for i in symbol:
        if i in x:
            return x[:x.find(i)]
columns = ['Temperature','Dew Point','Humidity','Wind Speed','Wind Gust','Pressure']
for clmn in columns:
    df[clmn] = df[clmn].apply(changesymbol)
df[['Temperature','Dew Point','Humidity','Wind','Wind Speed','Pressure']] = df[['Temperature','Dew Point','Humidity','Wind','Wind Speed','Pressure']].astype(float)
df.drop(df[df['Wind Speed']  > 8 ].index, inplace = True)
df.drop(df[df['Temperature'] < 1 ].index, inplace = True)
df.reset_index(drop=True,inplace=True)

df_Haze = df[df['Condition'] == 'Haze']
df_Cloudy = df[df['Condition'] == 'Mostly Cloudy']
df_Fog = df[df['Condition'] == 'Fog']
df_T_Storm = df[df['Condition'] == 'T-Storm']
df_Fair = df[df['Condition'] == 'Fair']
df_Rain = df[df['Condition'] == 'Rain']

df_new = df_Fog.append([df_Haze,df_Cloudy,df_T_Storm,df_Fair,df_Rain])

df_new.drop(['Precip.','Time','Month','Dates'], axis=1, inplace=True)
df_new.reset_index(drop=True,inplace=True)

df_new.drop(['Wind','Wind Gust'], axis=1, inplace=True)
values = df_new.drop(['Condition'], axis=1)
target = df_new.Condition

from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical

encoder = LabelEncoder()
encoder.fit(target)
target = encoder.transform(target)
target_ann = to_categorical(target)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# transform data
values = scaler.fit_transform(values)

X_train, X_test, y_train, y_test = train_test_split(values, target, test_size=1/3, random_state=10)
X_train_ann, X_test_ann, y_train_ann, y_test_ann = train_test_split(values, target_ann, test_size=1/3, random_state=10)

from sklearn.neighbors import KNeighborsClassifier

KNC = KNeighborsClassifier(n_neighbors=26)
KNC.fit(X_train, y_train)

def Bengaluru_KNC(lst):
    result = KNC.predict([lst])
    return encoder.inverse_transform(result)


from sklearn.tree import DecisionTreeClassifier
DTC = DecisionTreeClassifier()
DTC.fit(values, target)


def Bengaluru_DTC(lst):
    result = DTC.predict([lst])
    return encoder.inverse_transform(result)


from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=30, criterion='gini')
RFC.fit(X_train, y_train)


def Bengaluru_RFC(lst):
    result = RFC.predict([lst])
    return encoder.inverse_transform(result)


from sklearn.svm import SVC
svc = SVC(kernel='rbf')
svc.fit(X_train, y_train)


def Bengaluru_SVC(lst):
    result = svc.predict([lst])
    return encoder.inverse_transform(result)





def changemonth(x):
    dicts={}
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(1,13):
        dicts[i]=months[i-1]
    return dicts[x]

def Bengaluru_line_chart(model_temp,model_dew,model_hum,model_wind_sp,model_press):
    Bengaluru_dataset = df.copy()
    Bengaluru_dataset.drop_duplicates(subset=['Month'], inplace=True)
    Bengaluru_dataset.set_index(['Month'], inplace=True)
    dicts = {'Temperature': [float(model_temp)], 'Pressure': [float(model_press)], 'Humidity': [float(model_hum)],'Dew Point': [float(model_dew)], 'Wind Speed': [float(model_wind_sp)]}
    df2 = pd.DataFrame(dicts)

    df3 = pd.concat([Bengaluru_dataset, df2], ignore_index=True)
    df3 = df3.set_index([['01-January', '02-February', '03-March', '04-April', '05-May', '06-June', '07-July','08-August', '09-September', '10- October', '11-November', '12-December', 'new']])
    st.area_chart(df3[['Temperature', 'Pressure', 'Humidity', 'Dew Point', 'Wind Speed']],use_container_width=False, width=800)
