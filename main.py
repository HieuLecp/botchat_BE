import mysql.connector
from flask import *

from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/chatbot": {"origins": "*"}}, supports_credentials=True)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
from ChatBot import ChatBot
from flask import jsonify, request
#from gevent.wsgi import WSGIServer


app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/chatbot", methods=['POST', 'OPTIONS'])
def chatbot():
    if request.method == "OPTIONS":
        # Trả về response để trình duyệt hiểu rằng CORS được phép
        response = jsonify({"message": "CORS preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

    # Xử lý request POST chính
    usr_req = request.json.get('usr_req')  # Nhận dữ liệu từ request JSON
    print("User request:", usr_req)

    r = ChatBot()  # Tạo đối tượng chatbot
    bot_resp = r.Chat_with_Bot(usr_req)  # Lấy phản hồi từ chatbot

    print("Bot response:", bot_resp)
    
    # Trả về JSON có CORS headers
    response = jsonify({"bot_resp": bot_resp})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
    app.run(debug=True,port=5000,threaded=True)