# Reading tracking routes
from app.readings import readings_bp

# Placeholder - we'll add routes later
@readings_bp.route('/test')
def test():
    return "Readings blueprint is working" 