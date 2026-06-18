from flask import Flask
from config import Config
from models.user import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route("/")
def home():
    return "🚗 AutoRescue V2 Running Successfully"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)