from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def Home():
    return "welcom"

  
if __name__ == '__main__':
  app.run(host='0.0.0.0')
