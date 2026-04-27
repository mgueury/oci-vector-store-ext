
import os
import traceback
from flask import Flask
from flask import jsonify
from flask_cors import CORS

import oracledb

app = Flask(__name__)
CORS(app)

@app.route('/dept')
def dept():
    
    a = []
    try:
        conn = oracledb.connect(
          user=os.getenv('DB_USER'),
          password=os.getenv('DB_PASSWORD'),
          dsn=os.getenv('DB_URL'))
        print("Successfully connected to database", flush=True)
        cursor = conn.cursor()
        cursor.execute("SELECT deptno, dname, loc FROM dept")
        deptRows = cursor.fetchall()
        for row in deptRows:
            a.append( {"deptno": row[0], "dname": row[1], "loc": row[2]} )
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        print(e, flush=True)
    finally:
        cursor.close() 
        conn.close()  
    print(a, flush=True)     
    response = jsonify(a)
    response.status_code = 200
    return response   

@app.route('/info')
def info():
        return "Python - Flask - Oracle"          

if __name__ == "__main__":
    from waitress import serve    
    serve(app, host="0.0.0.0", port=8080)