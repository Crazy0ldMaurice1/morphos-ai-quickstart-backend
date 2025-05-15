import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Trusted origins for production and local dev
TRUSTED_ORIGINS = ['http://localhost:3000', 'https://your-production-domain.com']

@app.after_request
def apply_cors(response):
    origin = request.headers.get('Origin')
    if origin in TRUSTED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    return psycopg2.connect(db_url)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/hello')
def api_hello():
    db_url = os.getenv('DATABASE_URL')
    return jsonify({
        "env": None,
        "database": db_url,
        "message": "Hello from Flask API!"
    })

@app.route('/api/echo', methods=['POST'])
def api_echo():
    data = request.json
    text = data.get('text', '')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user_inputs (content) VALUES (%s)", (text,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"Saved: {text}"})

@app.route('/api/messages', methods=['GET'])
def api_get_messages():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, content FROM user_inputs")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        messages = [{"id": row[0], "content": row[1]} for row in rows]
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    app.run(debug=True)