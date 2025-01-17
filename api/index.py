import os
from flask import Flask, request, send_from_directory, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import date, time, datetime
from dotenv import load_dotenv

app = Flask(__name__)

env = os.environ.get('VERCEL_ENV', 'local')
load_dotenv(os.path.join(app.root_path, f'.env.{env}'))

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'c.html')

@app.route('/about')
def about():
    return 'Something about Sophia :)'

def convert_to_serializable(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    elif isinstance(obj, tuple):
        return [convert_to_serializable(i) for i in obj]
    else:
        return obj
        
def query(sql):
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get('PGDATABASE'),
            user=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD'),
            host=os.environ.get('PGHOST'),
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"columns": columns, "data": convert_to_serializable(result)}

    except Exception as e:
        return str(e)

@app.route('/db')
def sql():
    list_all_tables = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
    sql = request.args.get('sql', default=list_all_tables, type=str)
    result = query(sql)
    return jsonify(result)

@app.route('/currentUser')
def queryCurrentUser():
    sql = "SELECT * from users where id = 1"
    return query(sql)














if __name__ == '__main__':
    app.run(debug=True)
