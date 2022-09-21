import oracledb
import mysql.connector

user = "SYS"
password = "example"
dsn = "localhost:1521/xepdb1"


def get_data_from_oracle(user_, password_, dsn_):
    with oracledb.connect(user=user_, password=password_, dsn=dsn_,
                          mode=oracledb.AUTH_MODE_SYSDBA) as connection:
        with connection.cursor() as cursor:
            sql = """SELECT r.CARD_ID, rk.KEY_CODE FROM REG_KEY rk 
            LEFT JOIN REG r ON rk.REG_ID = r.REG_ID"""
            return cursor.execute(sql)


def delete_data_from_sql(user_, password_, host_):
    with mysql.connector.connect(host=host_,
                                 user=user_, password=password_) as connection:
        sql = "delete from personal where description = 'API_GUEST'"
        with connection.cursor() as cursor:
            cursor.execute(sql)


