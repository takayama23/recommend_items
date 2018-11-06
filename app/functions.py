import pandas as pd
import random
from datetime import datetime, timedelta
from random import randrange
from sqlalchemy import create_engine
from app import app


# 引数として渡されたSQLを実行し、データフレーム型で返す関数
def pd_sql_to_df(sql):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql(sql, engine)

    return df