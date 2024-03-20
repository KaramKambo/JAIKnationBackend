from flask_cors import CORS
from __init__ import app, db

from api.ML import ml_bp

from model.ML import init_ml

app.register_blueprint(ml_bp)

@app.before_first_request
def init_db():
    with app.app_context():
        db.create_all()
        init_ml()


if __name__ == "__main__":
    cors = CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8199")