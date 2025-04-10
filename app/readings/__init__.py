# Readings module initialization
from flask import Blueprint

readings_bp = Blueprint('readings', __name__, url_prefix='/readings')

from app.readings import routes 