# Group management routes
from app.groups import groups_bp

# Placeholder - we'll add routes later
@groups_bp.route('/test')
def test():
    return "Groups blueprint is working" 