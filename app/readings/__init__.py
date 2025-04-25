# Readings module initialization
from flask import Blueprint

readings_bp = Blueprint('readings', __name__, url_prefix='/readings')

# Use relative import for routes
from . import routes 