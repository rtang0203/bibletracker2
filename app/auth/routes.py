# Authentication routes 
from app.auth import auth_bp

# Placeholder - we'll add routes later
@auth_bp.route('/test')
def test():
    return "Auth blueprint is working"