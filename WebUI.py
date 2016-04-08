from flask import Flask, jsonify
from flask import render_template
from flask import request

import query


app = Flask(__name__)

@app.route('/reply', methods=['GET'])
def reply():
    #access your DB get your results here
    # print request.args.get("query")
    val = query.main(request.args.get("query"))
    data = {"value": val}
    return jsonify(data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='127.0.0.1', port=port)