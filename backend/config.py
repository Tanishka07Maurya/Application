import os
import pymysql

# try:
#     connection = pymysql.connect(
#         host='public-mysql-35ccb4d9-quizapplication.d.aivencloud.com',
#         user='avnadmin',
#         password='AVNS_IGyQyvOs9EJELlKx9h4',
#         database='dbquiz',
#         port=260565
#     )
#     print("Successfully connected to the database using PyMySQL!")

# except pymysql.MySQLError as e:
#     print(f"Failed to connect to the database: {e}")
    

class Config:
    # Database
    DB_HOST = os.environ.get('DB_HOST', 'public-mysql-35ccb4d9-quizapplication.d.aivencloud.com')
    DB_USER = os.environ.get('DB_USER', 'avnadmin')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'AVNS_IGyQyvOs9EJELlKx9h4')
    DB_DATABASE = os.environ.get('DB_DATABASE', 'dbquiz')
    DB_PORT = int(os.environ.get('DB_PORT', 26056))

    # SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    DEBUG = True
    SESSION_COOKIE_SECURE = True  
    
