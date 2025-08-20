from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Konthamandhi message chesay varak message kuda cheyaru endho emo dosthan"

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

