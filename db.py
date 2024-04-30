# db.py
import mysql.connector

mydb = mysql.connector.connect(
    host="",  # your host or IP address
    user="",  # your database username
    password="",  # your database password
    database="snippetbot"  # import snippetbot.sql DONT TOUCH
)


def insert_snippet(name, code_lang, code):
    try:
        cursor = mydb.cursor()
        sql = "INSERT INTO snippets (name, code_lang, code) VALUES (%s, %s, %s)"
        val = (name, code_lang, code)
        cursor.execute(sql, val)
        mydb.commit()
        return True
    except:
        return False


def retrieve_snippet(name):
    try:
        cursor = mydb.cursor()
        sql = "SELECT code_lang, code FROM snippets WHERE name = %s"
        val = (name,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        return result
    except:
        return None


def delete_snippet(name):
    try:
        cursor = mydb.cursor()
        sql = "DELETE FROM snippets WHERE name = %s"
        val = (name,)
        cursor.execute(sql, val)
        mydb.commit()
        return cursor.rowcount > 0
    except:
        return False

def get_all_snippet_names():
    try:
        cursor = mydb.cursor()
        sql = "SELECT name FROM snippets"
        cursor.execute(sql)
        results = cursor.fetchall()
        return [result[0] for result in results]
    except:
        return []