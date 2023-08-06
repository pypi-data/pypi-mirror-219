import time
from os import environ
from .db import DB, sql
from pandas import DataFrame

session_token_cookie_name = "uwtool_session_token"


def print_log(log_line):
    print(time.strftime('%Y-%m-%d %H:%M:%S'), log_line)


def ci(cursor, column_name):
    column_index_cnt = -1
    column_index = -1
    for column in cursor.description:
        column_index_cnt = column_index_cnt + 1
        if column[0] == column_name:
            column_index = column_index_cnt
            break
    if column_index == -1:
        raise SystemExit("ERROR: Column index not found for column: " + column_name)
    return column_index


def nvl(s, d):
    if s is None:
        return d
    else:
        return s


def iif(bool_val, ret_true, ret_false):
    if bool_val:
        aaa = ret_true
    else:
        aaa = ret_false
    return aaa


def isnullorempty(v):
    if v is None:
        return True
    if type(v) == str:
        v = v.strip()
        if len(v) == 0:
            return True
    return False


def clear_mfv(mfv):
    if type(mfv) == dict:
        for i in mfv.keys():
            mfv[i] = None
    return mfv


def get_username():
    conn_repserv = DB.get_connection('repserv')
    cursor_repserv = conn_repserv.cursor()

    username = None

    if 'HTTP_COOKIE' in environ:
        for cookie in map(str.strip, environ['HTTP_COOKIE'].split(';')):
            key, value = cookie.split('=')
            if key == session_token_cookie_name:
                uwtool_session_token = value
                result = DB.execute(cursor=cursor_repserv,
                                    query=sql("find_session", 2),
                                    fetch='one',
                                    parameters=uwtool_session_token)
                if result:  # can be replaced by "if cursor_repserv.rowcount"
                    username = result['username']
                    DB.execute(cursor_repserv, sql("update_session", 1), None, (uwtool_session_token, username))
                    cursor_repserv.commit()

    cursor_repserv.close()

    return username


def data_vector_to_sql_insert(data_vector: dict | DataFrame, insert_sql_tpl: str = None,
                              existing_values: list = None) -> (list, str):
    column_names_insert_text = ""
    item_values = []

    # convert data vector into a list
    if isinstance(data_vector, DataFrame):
        for column_name in data_vector.columns.tolist():
            column_names_insert_text = (column_names_insert_text + "," + column_name + "\r\n").replace(".", "_")
            item_values.append(data_vector.loc[0, column_name])

    elif type(data_vector) is dict:
        pass

    else:
        raise TypeError("data_vector_to_sql_insert: data_vector must be a pandas.DataFrame or a dictionary")

    # text-serialize any embedded lists or dictionaries
    item_values = [str(item_value) if type(item_value) in (list, dict) else item_value for item_value in item_values]

    # combine existing values with new values
    if type(existing_values) is list:
        result_items = existing_values + item_values
    elif existing_values is None:
        result_items = item_values
    else:
        raise TypeError("data_vector_to_sql_insert: existing_values must be a list or None")

    # generate SQL
    if type(insert_sql_tpl) is str:
        result_sql = insert_sql_tpl.format(column_names_insert_text, f"{', ?' * len(item_values)}")
    elif insert_sql_tpl is None:
        result_sql = column_names_insert_text
    else:
        raise TypeError("data_vector_to_sql_insert: insert_sql_tpl must be a string or None")

    return result_items, result_sql

