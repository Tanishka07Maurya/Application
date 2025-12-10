import pymysql
from flask import current_app

def get_db_connection():
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        db=current_app.config['DB_DATABASE'],
        port=current_app.config['DB_PORT'],
        cursorclass=pymysql.cursors.DictCursor
    )
