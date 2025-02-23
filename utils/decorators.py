import json
from flask_jwt_extended import get_jwt_identity

def role_required(*roles):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()

            # 🔥 Convert JSON string back to dictionary if needed
            if isinstance(current_user, str):
                current_user = json.loads(current_user)  # Deserialize JSON string

            if current_user.get('role_name') not in roles:
                return {"message": "Access forbidden: insufficient permissions"}, 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
