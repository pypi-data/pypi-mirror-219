import re
import traceback
import pymysql
import os
import sys
import pytest
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)

from LoggerLocalPythonPackage.MessageSeverity import MessageSeverity
from LoggerLocalPythonPackage.LocalLogger import _Local_Logger
load_dotenv()
logger_local=_Local_Logger
ID = 5000001
object_to_initlize={
    'client_ip_v4': 'ipv4-py',
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 33,
        'longitude': 35,
        'user_id': ID,
        'profile_id': ID,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'log from python -object_1',
        'component_id': ID,
        'variable_id': ID,
        'variable_value_old': 'variable_value_old-python',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
}
logger_local.init(object=object_to_initlize)


# Connect to the datbaase to validat that the log was inserted
def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        host=os.getenv('RDS_HOSTNAME'),
        database='logger' #os.getenv('RDS_DB_NAME')
    )
@pytest.mark.test
def test_log_with_only_logger_object():
    object_to_insert_1 = {
        'payload': 'log from python -object_1 check',
    }
    logger_local.info(object=object_to_insert_1)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_1['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value
@pytest.mark.test
def test_error_with_only_logger_object():
    object_to_insert_2 = {
        'payload': 'payload from error python -object_2',
    }
    logger_local.error(object=object_to_insert_2)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_2['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
@pytest.mark.test
def test_verbose_with_only_logger_object():
    object_to_insert_3 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 32,
        'longitude': 35,
        'variable_id': ID,
        'variable_value_old': 'variable_value_old-python-object_3',
        'variable_value_new': 'variable_value_new-python',
    }
    logger_local.verbose(object=object_to_insert_3)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE variable_value_old = '{object_to_insert_3['variable_value_old']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Verbose.value
@pytest.mark.test
def test_warn_with_only_logger_object():
    object_to_insert_4 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 32,
        'longitude': 35,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'payload from python -object_4',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
    }
    logger_local.warn(object=object_to_insert_4)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_4['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Warning.value
@pytest.mark.test
def test_add_message():
    # option to insert only message
    message = 'only message error from python'
    logger_local.error(message)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{message}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
@pytest.mark.test
def test_debug_with_only_logger_object():
    object_to_insert5={
       'payload':"Test python!!! check for debug insert"
    }
    logger_local.debug(object=object_to_insert5)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert5['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Debug.value
@pytest.mark.test
def test_start_with_only_logger_object():
    object_to_insert6={
       'payload':"Test python!!! check for start insert"
    }
    logger_local.start(object=object_to_insert6)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert6['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Start.value
@pytest.mark.test
def test_end_with_only_logger_object():
    object_to_insert7={   
       'payload':"Test python!!! check for end insert",
    }
    logger_local.end(object=object_to_insert7)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert7['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.End.value
@pytest.mark.test
def test_init_with_only_logger_object():  
    logger_local.init("Test python!!! check for init insert")
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = 'Test python!! check for init insert' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Init.value

@pytest.mark.test
def test_exception_with_only_logger_object():
    try:
        x = 5 / 0
    except Exception as e:
        logger_local.exception(object=e)
        stack_trace = str(traceback.format_exception(type(e), e, e.__traceback__))

    conn = get_connection()
    cursor = conn.cursor()

    escaped_stack_trace = re.escape(stack_trace)
    pattern = f"%{escaped_stack_trace}%"
    sql = "SELECT severity_id FROM logger.logger_table WHERE error_stack LIKE %s ORDER BY timestamp DESC LIMIT 1;"
    cursor.execute(sql, (pattern,))

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Exception.value
   
@pytest.mark.test
def test_error():
    object_to_insert9={   
       'payload': 'payload from error python -object_9'
       
    }
    msg="check for error with both object and message"
    logger_local.error(msg,object=object_to_insert9)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert9['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
    assert result[1]== msg
@pytest.mark.test
def test_start():
    object_to_insert10={   
       'payload': 'payload from start python -object_10'
       
    }
    msg="check for start with both object and message"
    logger_local.start(msg,object=object_to_insert10)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert10['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Start.value
    assert result[1]== msg
@pytest.mark.test
def test_End():
    object_to_insert11={   
       'payload': 'payload from end python -object_11'
       
    }
    msg="check for end with both object and message"
    logger_local.end(msg,object=object_to_insert11)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert11['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.End.value
    assert result[1]== msg
@pytest.mark.test
def test_debug():
    object_to_insert12={   
       'payload': 'payload from debug python -object_12'
       
    }
    msg="check for debug with both object and message"
    logger_local.debug(msg,object=object_to_insert12)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert12['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Debug.value
    assert result[1]== msg
@pytest.mark.test
def test_log():
    object_to_insert13={   
       'payload': 'payload from info python -object_13'
       
    }
    msg="check for info with both object and message"
    logger_local.info(msg,object=object_to_insert13)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert13['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value
    assert result[1]== msg
@pytest.mark.test
def test_Init():
    object_to_insert14={   
       'payload': 'payload from init python -object_14'
       
    }
    msg="check for init with both object and message"
    logger_local.init(msg,object=object_to_insert14)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert14['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Init.value
    assert result[1]== msg

@pytest.mark.test
def test_Exception():
    try:
        x = 5 / None
    except Exception as e:
        logger_local.exception("exception check",object=e)
        stack_trace = str(traceback.format_exception(type(e), e, e.__traceback__))
    conn = get_connection()
    cursor = conn.cursor()

    escaped_stack_trace = re.escape(stack_trace)
    pattern = f"%{escaped_stack_trace}%"
    sql = "SELECT severity_id,message FROM logger.logger_table WHERE error_stack LIKE %s ORDER BY timestamp DESC LIMIT 1;"
    cursor.execute(sql, (pattern,))
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Exception.value
    assert result[1]=="exception check"
@pytest.mark.test
def test_component_id():
    object_to_insert8={   
       'payload':"Test python!! check for logger without init before",
       'component_id': 101,
       
    }
    _Local_Logger.clean_variables()
    _Local_Logger.info(object=object_to_insert8)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,component_id FROM logger.logger_table WHERE payload = '{object_to_insert8['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value
    assert result[1]== 101
