from flask import Blueprint

icicle_flaskn = Blueprint('iciflaskn', __name__, template_folder='templates')
from iciflaskn import routes