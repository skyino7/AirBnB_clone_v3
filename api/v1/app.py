#!/usr/bin/python3
"""
Status of your API
"""
from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of the request"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
