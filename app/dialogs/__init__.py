from flask import Blueprint

bp = Blueprint('dialogs', __name__)

from app.dialogs import routes