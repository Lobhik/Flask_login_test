from flask import Flask, jsonify
from flask_cors import CORS
from urls.user.user import user_bp
from urls.test_urls.test_urls import test_bp



app = Flask(__name__)


CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, PATCH, POST, GET, DELETE')
    response.headers.add('Access-Control-Allow-Headers','access-control-allow-headers,content-type,Access-Control-Allow-Origin,access-control-max-age,username,password, content-type,auth_token,crossorigin')
    return response

'''
  API Default Route
'''
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
  return jsonify({'message': "Hello lobhik ?"}), 200

# @app.route('/')
# def hello_world():
#     return 'Hello World'

app.register_blueprint(user_bp,url_prefix="/user")
app.register_blueprint(test_bp,url_prefix="/test")



# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

