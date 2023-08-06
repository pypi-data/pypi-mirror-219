import os
import dotenv 
from LoggerLocalPythonPackage.LocalLogger import _Local_Logger
import mysql.connector
dotenv.load_dotenv()
from config import db_connection

Local_Logger=_Local_Logger
class library_DB:
    def __init__(self):
        self.conn = db_connection()
        self.cursor = self.conn.cursor()
        
    def insert_User_Access_Token(self,user_name,profile_id,access_token):
        try:
            Local_Logger.start("START insert access token to db "+access_token) 
            cursor = self.conn.cursor()
            query_max_id = "SELECT MAX(id) FROM external_user.external_user_table"
            cursor.execute(query_max_id)
            res = cursor.fetchone()
            cursor.close()
            max_id = res[0] + 1
            cursor = self.conn.cursor() 
            query_insert_external = "INSERT INTO external_user.external_user_table (id,system_id,username,token) VALUES (%s,1,%s,%s)"
            values=(max_id,user_name,access_token)
            cursor.execute(query_insert_external, values)
            self.conn.commit()  
            cursor.close()
            cursor = self.conn.cursor()     
            query_max_id = "SELECT MAX(id) FROM external_user_profile.external_user_profile_table"
            cursor.execute(query_max_id)
            res = cursor.fetchone()
            cursor.close()
            if(res[0]):
                max_id_new = res[0] + 1
            else:
                max_id_new=1
            cursor = self.conn.cursor() 
            values=(max_id_new,max_id,profile_id)
            query_insert_external_user_profile= "INSERT INTO external_user_profile.external_user_profile_table (id,external_user_id,profile_id) VALUES (%s,%s,%s)"
            cursor.execute(query_insert_external_user_profile,values)
            cursor.close()
            self.conn.commit()
            Local_Logger.end("END insert access token to db")
        except mysql.connector.Error as error:
            Local_Logger.exception(error)
            
    def get(self,user_name):
        try:
            Local_Logger.start("start get access token for "+user_name) 
            cursor = cursor = self.conn.cursor()
            query_get_all = "SELECT token FROM external_user.external_user_table WHERE username=%s"
            cursor.execute(query_get_all,(user_name,))
            res = cursor.fetchone()
            Local_Logger.end("END get access token from db")
            return res
        except mysql.connector.Error as error:
            Local_Logger.exception(error)
    
    def select_by_profile_id(self,profile_id):
        try:
            Local_Logger.start("start get access token") 
            cursor = self.conn.cursor()

            # Execute the select query
            select_query = """
                SELECT * 
                FROM external_user.external_user_table AS eu 
                JOIN external_user_profile.external_user_profile_table AS eup ON eu.id = eup.external_user_id 
                WHERE eup.profile_id = %s
            """
            cursor.execute(select_query, (profile_id,))
            result = cursor.fetchone()
            cursor.close()
            Local_Logger.end("END get access token from db")
            return result
        except mysql.connector.Error as error:
            Local_Logger.exception(error)

        # Fetch all the rows returned by the query
            
    
    def update_by_user_name(self,user_name,access_token):
        try:
            Local_Logger.start("start update access token for "+user_name)
            cursor = self.conn.cursor()
            update_query = "UPDATE external_user.external_user_table SET token = %s WHERE username = %s"
            values = (access_token, user_name)
            cursor.execute(update_query, values)
            self.conn.commit()
            cursor.close()
            Local_Logger.end("END update access token in db")
        except mysql.connector.Error as error:
            Local_Logger.exception(error)



    def update_by_profile_id(self,profile_id, access_token):
        try:
            Local_Logger.start("start update access token ")
            cursor = self.conn.cursor()

            update_query = """
                UPDATE external_user.external_user_table 
                SET token = %s 
                WHERE id IN (
                    SELECT external_user_id 
                    FROM external_user_profile.external_user_profile_table 
                    WHERE profile_id = %s
                )
            """
            values = (access_token, profile_id)
            cursor.execute(update_query, values)
            self.conn.commit()
            cursor.close()
            Local_Logger.end("update access token in db")
        except mysql.connector.Error as error:
           Local_Logger.exception(error)
        
    def delete_by_profile_id(self,profile_id):
        try:
            Local_Logger.start("delete user external access token ")
            # Create a cursor object to execute queries
            cursor = self.conn.cursor()
            delete_query = """
                UPDATE external_user.external_user_table AS eu
                JOIN external_user_profile.external_user_profile_table AS eup ON eu.id = eup.external_user_id
                SET eu.id = NULL, eu.system_id = NULL, eu.username = NULL, eu.token = NULL, eup.profile_id = NULL
                WHERE eup.profile_id = %s
            """
            cursor.execute(delete_query, (profile_id,))

            self.conn.commit()

            cursor.close()
            Local_Logger.end("delete access token from db")
        except mysql.connector.Error as error:
           Local_Logger.exception(error)
            
    



        