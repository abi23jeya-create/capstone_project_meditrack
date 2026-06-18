from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required
from .. import db
from ..models import Equipment, MaintenanceRecord, WorkOrder, SparePart

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def report_center():
    maintenance_costs = db.session.query(Equipment.asset_tag, db.func.coalesce(db.func.sum(MaintenanceRecord.cost), 0)).outerjoin(MaintenanceRecord).group_by(Equipment.id).all()
    work_order_counts = db.session.query(WorkOrder.status, db.func.count(WorkOrder.id)).group_by(WorkOrder.status).all()
    low_stock = SparePart.query.filter(SparePart.quantity <= SparePart.reorder_level).all()
    return render_template('reports.html', maintenance_costs=maintenance_costs, work_order_counts=work_order_counts, low_stock=low_stock, today=date.today())
