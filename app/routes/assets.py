from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..forms import EquipmentForm
from ..models import Equipment, EquipmentCategory, Manufacturer, Department, Location, EquipmentTransfer
from ..utils import permission_required, log_audit

assets_bp = Blueprint('assets', __name__)

def _populate(form):
    form.category_id.choices = [(c.id, c.name) for c in EquipmentCategory.query.order_by(EquipmentCategory.name).all()]
    form.manufacturer_id.choices = [(m.id, m.name) for m in Manufacturer.query.order_by(Manufacturer.name).all()]
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by(Department.name).all()]
    form.location_id.choices = [(l.id, f'{l.department.name} / Room {l.room_number} / Bed {l.bed_number or "-"}') for l in Location.query.all()]

@assets_bp.route('/')
@login_required
@permission_required('manage_assets')
def equipment_list():
    department = request.args.get('department', '')
    status = request.args.get('status', '')
    query = Equipment.query
    if department:
        query = query.join(Department).filter(Department.name == department)
    if status:
        query = query.filter(Equipment.current_status == status)
    equipment = query.order_by(Equipment.asset_tag).all()
    departments = Department.query.order_by(Department.name).all()
    statuses = ['Active', 'In Use', 'Available', 'Under Maintenance', 'Out of Service', 'Retired', 'Lost']
    return render_template('equipment_list.html', equipment=equipment, departments=departments, statuses=statuses)

@assets_bp.route('/new', methods=['GET', 'POST'])
@login_required
@permission_required('manage_assets')
def new_equipment():
    form = EquipmentForm()
    _populate(form)
    if form.validate_on_submit():
        eq = Equipment(**{field: getattr(form, field).data for field in ['asset_tag','serial_number','category_id','manufacturer_id','model_number','purchase_date','warranty_expiry','current_status','criticality_level','department_id','location_id']})
        db.session.add(eq)
        db.session.commit()
        log_audit(current_user.id, 'CREATE', 'equipment', eq.id, '', eq.asset_tag)
        flash('Equipment created successfully.', 'success')
        return redirect(url_for('assets.equipment_list'))
    return render_template('equipment_form.html', form=form, title='Add Equipment')

@assets_bp.route('/<int:equipment_id>')
@login_required
def equipment_detail(equipment_id):
    eq = Equipment.query.get_or_404(equipment_id)
    return render_template('equipment_detail.html', equipment=eq)

@assets_bp.route('/<int:equipment_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('manage_assets')
def edit_equipment(equipment_id):
    eq = Equipment.query.get_or_404(equipment_id)
    form = EquipmentForm(obj=eq)
    _populate(form)
    if form.validate_on_submit():
        old_status = eq.current_status
        form.populate_obj(eq)
        db.session.commit()
        log_audit(current_user.id, 'UPDATE', 'equipment', eq.id, old_status, eq.current_status)
        flash('Equipment updated.', 'success')
        return redirect(url_for('assets.equipment_detail', equipment_id=eq.id))
    return render_template('equipment_form.html', form=form, title='Edit Equipment')

@assets_bp.route('/<int:equipment_id>/transfer', methods=['POST'])
@login_required
@permission_required('manage_assets')
def transfer_equipment(equipment_id):
    eq = Equipment.query.get_or_404(equipment_id)
    to_location = Location.query.get_or_404(int(request.form['location_id']))
    record = EquipmentTransfer(equipment_id=eq.id, from_location=f'{eq.location.department.name} / {eq.location.room_number}', to_location=f'{to_location.department.name} / {to_location.room_number}', transferred_by=current_user.id)
    eq.location_id = to_location.id
    eq.department_id = to_location.department_id
    db.session.add(record)
    db.session.commit()
    flash('Equipment transferred successfully.', 'success')
    return redirect(url_for('assets.equipment_detail', equipment_id=eq.id))
