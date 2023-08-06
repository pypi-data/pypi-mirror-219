from locdataMAC.logger import logger
from locdataMAC.cutom_exception import InvalidpathException
from ensure import ensure_annotations
import pandas as pd
import plotly.express as px


def hour_convvertor(x):
    json_data=x
    hour=0
    for i in json_data:
        total=round(i['hours']+(i['minutes']/60)+(i['seconds']/(60*60)),5)
        hour=hour+total
    return hour

@ensure_annotations
def mydata_analysis(path:str):
    df= pd.read_json(path)
    df['time_spent'] = df.time_entries.apply(hour_convvertor)
    df.drop(['time_entries'],axis='columns',inplace=True)
    fig = px.bar(df, x='name', y='time_spent')
    df_sorted = df.sort_values('time_spent',ascending=False)
    fig1 = px.bar(df_sorted.head(3), x='name', y='time_spent')
    return fig.show(),fig1.show()