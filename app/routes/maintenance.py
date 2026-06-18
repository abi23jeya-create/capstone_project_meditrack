from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .. import db
from ..forms import WorkOrderForm, MaintenanceForm
from ..models import WorkOrder, Equipment, Technician, MaintenanceRecord
from ..utils import permission_required

maintenance_bp = Blueprint('maintenance', __name__)

def _populate_workorder(form):
    form.equipment_id.choices = [(e.id, f'{e.asset_tag} - {e.serial_number}') for e in Equipment.query.order_by(Equipment.asset_tag).all()]
    form.assigned_to.choices = [(0, 'Unassigned')] + [(t.id, t.name) for t in Technician.query.order_by(Technician.name).all()]


def _populate_maintenance(form):
    form.equipment_id.choices = [(e.id, f'{e.asset_tag} - {e.serial_number}') for e in Equipment.query.order_by(Equipment.asset_tag).all()]
    form.work_order_id.choices = [(0, 'No linked work order')] + [(w.id, f'WO-{w.id} / {w.status}') for w in WorkOrder.query.order_by(WorkOrder.id.desc()).all()]

@maintenance_bp.route('/work-orders')
@login_required
@permission_required('manage_maintenance')
def work_orders():
    items = WorkOrder.query.order_by(WorkOrder.created_date.desc()).all()
    return render_template('work_orders.html', items=items)

@maintenance_bp.route('/work-orders/new', methods=['GET', 'POST'])
@login_required
@permission_required('manage_maintenance')
def new_work_order():
    form = WorkOrderForm()
    _populate_workorder(form)
    if form.validate_on_submit():
        assigned = None if form.assigned_to.data == 0 else form.assigned_to.data
        wo = WorkOrder(equipment_id=form.equipment_id.data, priority=form.priority.data, status=form.status.data, issue_description=form.issue_description.data, assigned_to=assigned)
        db.session.add(wo)
        db.session.commit()
        flash('Work order created.', 'success')
        return redirect(url_for('maintenance.work_orders'))
    return render_template('work_order_form.html', form=form)

@maintenance_bp.route('/records')
@login_required
def maintenance_records():
    records = MaintenanceRecord.query.order_by(MaintenanceRecord.date_performed.desc()).all()
    return render_template('maintenance_records.html', records=records)

@maintenance_bp.route('/records/new', methods=['GET', 'POST'])
@login_required
@permission_required('manage_maintenance')
def new_record():
    form = MaintenanceForm()
    _populate_maintenance(form)
    if form.validate_on_submit():
        work_order_id = None if form.work_order_id.data == 0 else form.work_order_id.data
        record = MaintenanceRecord(equipment_id=form.equipment_id.data, work_order_id=work_order_id, maintenance_type=form.maintenance_type.data, date_performed=form.date_performed.data, findings=form.findings.data, actions_taken=form.actions_taken.data, cost=form.cost.data or 0, next_due_date=form.next_due_date.data)
        db.session.add(record)
        db.session.commit()
        flash('Maintenance record saved.', 'success')
        return redirect(url_for('maintenance.maintenance_records'))
    return render_template('maintenance_form.html', form=form)
