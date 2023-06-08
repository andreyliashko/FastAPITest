import asyncio

import psycopg2

import config
import scremas
from config import *
from fastapi import FastAPI

app = FastAPI()


def connect_toDatabase(dbase_name: str):
    connect = None
    try:
        # connect to postgreSql database
        connect = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbase_name
        )
        connect.autocommit = True

    except Exception as ex:
        print('[INFO] An occur when connect to database')
        print(ex.__str__())

    return connect


# get database name
@app.get('/')
async def getCurrentDatabase():
    return db_name


# get all student list sort by asc
@app.get('/students')
async def getAllStudent():
    result = None
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute("""SELECT * FROM students ORDER BY user_id;""")
        result = cursor.fetchall()
    return result


# add student with StudentModel attributes
@app.post('/addStudent')
async def addStudent(input_student: scremas.StudentModel):
    result = None
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute(
            """INSERT INTO students(user_id, name, surname, item_id) VALUES (%s,%s, %s, %s);""",
            (input_student.user_id, input_student.name, input_student.surname, input_student.item_id)
        )
        result = "student added"
    return result


# get user by their id
@app.get('/user/{input_id}/')
async def getUserById(input_id: int):
    result = None
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute("""SELECT s.* FROM students s WHERE s.user_id = %s;""", (input_id,))

        result = cursor.fetchone()
    return result


# check if user exist in database
@app.get('/findUser/{st_id}')
async def findUser(st_id: int):
    status = None
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute("""SELECT EXISTS(SELECT user_id FROM students WHERE user_id = %s );""", (st_id,))
        status = cursor.fetchone()
    return status


# delete user by input id
@app.delete('/deleteUserById/{input_id}')
async def deleteUserById(input_id: int):
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute("""SELECT EXISTS(SELECT user_id FROM students WHERE user_id = %s );""", (input_id,))
        status = cursor.fetchone()
        if not status[0]:
            return "Student doesn`t exist"
        cursor.execute("""DELETE FROM students WHERE user_id = %s;""", (input_id,))
        return f"Student  with id={input_id} deleted"
    return "[INFO] Can`t connect to database"


# change field to new_data of some student with input_id at any column number
# can`t change user id
@app.get('/changeField/{input_id}/{column}/{new_data}/')
@app.patch('/changeField/{input_id}/{column}/{new_data}/')
async def changeField(input_id: int, column: int, new_data: str):
    with connect_toDatabase(db_name).cursor() as cursor:
        cursor.execute("""SELECT EXISTS(SELECT user_id FROM students WHERE user_id = %s );""", (input_id,))
        status = cursor.fetchone()
        if not status[0]:
            return f"Student with id={input_id} doesn`t exist"
        cursor.execute("""SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_catalog = %s AND table_name = 'students';""", (config.db_name,))

        columns_size = int(cursor.fetchone()[0])
        if column > columns_size - 1 or column < 1:
            return f"[INFO] Can`t find {column}-column/ Choose parameter from 1 to {columns_size - 1}"
        cursor.execute("""SELECT Column_name FROM Information_schema.columns WHERE Table_name like 'students';""")
        current_row = cursor.fetchall()[column][0]
        cursor.execute(f"""UPDATE students SET {current_row} = %s WHERE  user_id = %s;""", (new_data, input_id))

        cursor.execute("""SELECT * FROM students WHERE user_id = %s;""", (input_id,))
        return cursor.fetchone()

    return "[INFO] Can`t connect to database"
