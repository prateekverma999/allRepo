# import logging
from fastapi import FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


@app.get('/dbconnection', status_code=status.HTTP_202_ACCEPTED)
def get():
    '''
    This API use to connect database!
    '''
    while True:
        try:
            conn = psycopg2.connect(host = '172.31.248.137',database = 'fastapi_1' ,user= 'postgres',
                        password = 'admin1', cursor_factory = RealDictCursor)
            cursor = conn.cursor()
            break
        except Exception as error:
            er = str(error).split('FATAL:')[-1].strip()
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Error: {er}")

    return 'Database connection was succesfull!'