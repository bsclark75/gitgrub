from flask import Flask
from seed import init_db    

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, GitGrub!'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
   