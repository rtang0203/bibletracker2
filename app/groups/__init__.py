# Groups module initialization
from flask import Blueprint

groups_bp = Blueprint('groups', __name__, url_prefix='/groups')

# Import routes at the end to potentially avoid circular dependencies during initialization
from . import routes # Use relative import 