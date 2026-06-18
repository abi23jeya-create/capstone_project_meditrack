from datetime import date
from flask import Blueprint, render_template
from ..models import Equipment, WorkOrder, MaintenanceRecord, SparePart, equipment_overdue_query
from .. import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    total_equipment = Equipment.query.count()
    status_counts = db.session.query(Equipment.current_status, db.func.count(Equipment.id)).group_by(Equipment.current_status).all()
    overdue = equipment_overdue_query().all()
    open_work_orders = WorkOrder.query.filter(WorkOrder.status.in_(['Open', 'Assigned', 'In Progress'])).count()
    low_stock = SparePart.query.filter(SparePart.quantity <= SparePart.reorder_level).count()
    maintenance_cost = db.session.query(db.func.coalesce(db.func.sum(MaintenanceRecord.cost), 0)).scalar()
    return render_template('dashboard.html', total_equipment=total_equipment, status_counts=status_counts, overdue=overdue, open_work_orders=open_work_orders, low_stock=low_stock, maintenance_cost=maintenance_cost, today=date.today())
