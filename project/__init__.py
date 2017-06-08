from flask import Flask

app = Flask(__name__)

from project.hotels.views import hotels_blueprint

app.register_blueprint(hotels_blueprint, url_prefix='/hotels')