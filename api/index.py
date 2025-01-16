import os
from flask import Flask, request, send_from_directory, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'c.html')

@app.route('/about')
def about():
    return 'Something about Sophia :)'

def query(sql):
    try:
        connection = psycopg2.connect(
            dbname="neondb",
            user="neondb_owner",
            password="QiNF8r1RdzMg",
            host="ep-green-butterfly-a5cxkofz-pooler.us-east-2.aws.neon.tech",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"columns": columns, "data": users}
    except Exception as e:
        return str(e)

@app.route('/db')
def sql():
    list_all_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
    sql = request.args.get('sql', default=list_all_tables, type=str)
    users = query(sql)
    return jsonify(users)
