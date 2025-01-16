from flask import Flask, send_from_directory
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'c.html')

@app.route('/about')
def about():
    return 'About Sophia, she is a tiger not a puma.'

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