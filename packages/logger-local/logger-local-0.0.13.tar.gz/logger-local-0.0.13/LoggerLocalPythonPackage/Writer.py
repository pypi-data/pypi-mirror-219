import pymysql
import mysql.connector
import os
from dotenv import load_dotenv
from circles_local_database_python.database import database
load_dotenv()

os_debug = os.getenv('DEBUG')
if(os_debug=='True' or os_debug=='1'):
    debug = True
else:
    debug = False
if (debug): print ("Writer.py debug is on debug=", debug)

class Writer:
    
    def get_connection(self) -> pymysql.connections.Connection:
        if (debug): print ("get_connection")
        database1=database()
        result=database1.connect_to_database()
        return result


    def add(self, **kwargs):
        connection=None
        try:
            params_to_insert = kwargs['object']
            # creating connection
            connection = self.get_connection()
            # connection = self._pool.get_connection()
            cursor = connection.cursor()

            try:
                if params_to_insert['latitude'] is None:
                    params_to_insert['latitude'] = 0
                if params_to_insert['longitude'] is None:
                    params_to_insert['longitude'] = 0
            except Exception as e:
                params_to_insert['latitude'] = 0
                params_to_insert['longitude'] = 0
            cursor.execute(
                f"insert into location.location_table (coordinate) values (POINT({params_to_insert['latitude'] if params_to_insert['latitude'] != None else 0},{params_to_insert['longitude'] if params_to_insert['longitude'] != None else 0}));")
            coordinate_id = cursor.lastrowid

            params_to_insert.pop('latitude')
            params_to_insert.pop('longitude')

            params_to_insert['location_id'] = coordinate_id
            listed_values = list(params_to_insert.values())
            joined_keys = ','.join(list(params_to_insert.keys()))
            generate_values_pattern = ','.join(['%s' for i in range(len(listed_values))])
            sql = f"""INSERT INTO logger.logger_table ({joined_keys})
                        VALUES ({generate_values_pattern});
            """
            cursor=connection.cursor()
            cursor.execute(sql,listed_values)
        except Exception as e:
            print("catched " + str(e))
        finally:
            if(connection):
                connection.commit()
                cursor.close()
                connection.close()

    def add_message(self, message, log_level):
        if (debug): print ("add_message" + message+ ' ' + str(log_level))
        connection=None
        try:
            # creating connection
            connection = self.get_connection()
            # connection = self._pool.get_connection()
            cursor = connection.cursor()
            sql = f"INSERT INTO logger.logger_table (payload, severity_id) VALUES ('{message}', {log_level})"
            cursor.execute(sql)

        except Exception as e:
            print("Writer.py Writer.add_message catched" + str(e))
        finally:
            if(connection):
                connection.commit()
                cursor.close()
                connection.close()
