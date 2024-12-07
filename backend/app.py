from flask import Flask
from flask_cors import CORS
from .api.search_stock import search_routes

import os


app = Flask(__name__)


CORS(app)

app.register_blueprint(search_routes,url_prefix='/api/search')



if __name__ == '__main__':
    app.run(debug=True)
    
