from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

def query_users():
    try:
        connection = psycopg2.connect(
            dbname="neondb",
            user="neondb_owner",
            password="QiNF8r1RdzMg",
            host="ep-green-butterfly-a5cxkofz-pooler.us-east-2.aws.neon.tech",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
    except Exception as e:
        return str(e)

@app.route('/users')
def users():
    users = query_users()
    return {'users': users}