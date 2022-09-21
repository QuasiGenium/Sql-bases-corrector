import oracledb
import mysql.connector

user = "SYS"
password = "example"
dsn = "localhost:1521/xepdb1"
tabid = 999999999


def get_data_from_oracle(user_, password_, dsn_):
    with oracledb.connect(user=user_, password=password_, dsn=dsn_,
                          mode=oracledb.AUTH_MODE_SYSDBA) as connection:
        with connection.cursor() as cursor:
            sql = """SELECT r.CARD_ID, rk.KEY_CODE FROM CLUB.REGISTRATION_KEYS
             rk LEFT JOIN CLUB.R_KEYS r ON rk.REG_ID = r.REG_ID"""
            return cursor.execute(sql).fetchall()


def delete_data_from_sql(user_, password_, host_):
    with mysql.connector.connect(host=host_,
                                 user=user_, password=password_) as connection:
        sql = "DELETE from service.personal where description = 'API_GUEST'"
        with connection.cursor() as cursor:
            cursor.execute(sql)


def transform_key(value):
    return '380' + f'{int(value):x}'.upper()


def put_key_to_sql(user_sql, password_sql, host_sql, user_oracle, password_oracle, dsn_oracle):
    with mysql.connector.connect(host=host_sql,
                                 user=user_sql, password=password_sql) as connection:
        cards_n_keys = get_data_from_oracle(user_oracle, password_oracle, dsn_oracle)
        with connection.cursor() as cursor:
            for i in cards_n_keys:
                something_cool = transform_key(i[1])
                cursor.execute(f'insert into personal(PARENT_ID,TYPE,EMP_TYPE,NAME,'
                               f'DESCRIPTION,STATUS,CODEKEY,CODEKEYTIME,CODEKEY_DISP_FORMAT,'
                               f"CREATEDTIME,BADGE,USER_APPLS_EDIT_CURRENT) "
                               f"values((select p.id from personal p where p.TABID = '{tabid}')"
                               f',"EMP","GUEST","{i[0]}","API_GUEST","AVAILABLE",'
                               f"x'{something_cool}'"
                               f',now(),"W58DEC",now(),"2","1")')

