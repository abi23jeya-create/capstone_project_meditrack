from datetime import date
from flask import Blueprint, jsonify
from flask_login import login_required
from ..models import equipment_overdue_query

api_bp = Blueprint('api', __name__)

@api_bp.route('/overdue-maintenance')
@login_required
def overdue_maintenance():
    items = equipment_overdue_query().all()
    payload = []
    for equipment in items:
        payload.append({
            'equipment_id': equipment.id,
            'asset_tag': equipment.asset_tag,
            'serial_number': equipment.serial_number,
            'status': equipment.current_status,
            'department': equipment.department.name,
            'next_due_date': str(equipment.latest_next_due) if equipment.latest_next_due else None,
            'is_overdue': bool(equipment.latest_next_due and equipment.latest_next_due < date.today())
        })
    return jsonify(payload)
