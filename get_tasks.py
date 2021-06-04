"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor


def get_tasks():
    cursor, _ = get_cursor()
    """Returns new tasks from databse (table tasks)"""
    try:
        cursor.execute("INSERT INTO  tasks (id, channel_id, added_on) VALUES   (2, 'sadsadsad', NOW())")
        cursor.execute("SELECT * FROM tasks")
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error:Failed getting new tasks from database")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    time.sleep(5)
    r = get_redis()
    q = Queue('get_tasks', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r, name='get_tasks')
        worker.work()
