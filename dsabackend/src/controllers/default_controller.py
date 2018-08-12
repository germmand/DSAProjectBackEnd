from flask import Blueprint

DefaultController = Blueprint('DefaultController', __name__)

@DefaultController.route('/')
def index():
    return "API is up and running! :)"
