from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Hello, this is Flask running on LAN"
if __name__ == '__main__':
    app.run(host="10.177.66.144",port=5000,debug=True)