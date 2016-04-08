from flask import Flask, jsonify
from flask import render_template

import query


app = Flask(__name__)

@app.route('/sampleurl', methods=['GET'])
def samplefunction():
    #access your DB get your results here
    val = query.main('What is the price of Cable Wholesale')
    print val
    data = {"value": val}
    return jsonify(data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='127.0.0.1', port=port)