from functools import wraps
from flask import abort
from flask_login import current_user
from . import db
from .models import AuditLog

def permission_required(code):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(code):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_audit(user_id, action, table_name, record_id, old_value='', new_value=''):
    entry = AuditLog(user_id=user_id, action=action, table_name=table_name, record_id=str(record_id), old_value=str(old_value), new_value=str(new_value))
    db.session.add(entry)
    db.session.commit()
