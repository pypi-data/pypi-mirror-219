import pymysql
from typing import Union

class Database:
    def __init__(self, host: str, port: int, username: str, password: str, database: str) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        
    def _connect(self) -> Union[pymysql.Connection, bool]:
        try:
            conn = pymysql.connect(
                user=self.__username,
                password=self.__password,
                host=self.__host,
                port=self.__port,
                database=self.__database
            )
            conn.autocommit(True)

        except Exception as e:
            print("An error occured while connecting")
            print(e)
            return
            
        return conn


    def execute(self, query: str, values: list = []) -> list[tuple]:
        conn = self._connect()
        if not conn:
            return []

        cur = conn.cursor()

        cur.execute(query, values)

        data = []
        try:
            data = cur.fetchall()

        except:
            pass

        try:
            conn.close()

        except:
            pass

        return data