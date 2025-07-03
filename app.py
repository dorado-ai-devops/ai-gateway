from flask import Flask
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
