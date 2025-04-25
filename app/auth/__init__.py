# Authentication module initialization 
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Use relative import for routes
from . import routes