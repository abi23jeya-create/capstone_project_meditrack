from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .. import db
from ..forms import SparePartForm
from ..models import SparePart, Vendor
from ..utils import permission_required

inventory_bp = Blueprint('inventory', __name__)

def _populate(form):
    form.vendor_id.choices = [(v.id, v.name) for v in Vendor.query.order_by(Vendor.name).all()]

@inventory_bp.route('/spare-parts')
@login_required
@permission_required('manage_inventory')
def spare_parts():
    parts = SparePart.query.order_by(SparePart.name).all()
    return render_template('spare_parts.html', parts=parts)

@inventory_bp.route('/spare-parts/new', methods=['GET', 'POST'])
@login_required
@permission_required('manage_inventory')
def new_spare_part():
    form = SparePartForm()
    _populate(form)
    if form.validate_on_submit():
        part = SparePart(name=form.name.data, part_number=form.part_number.data, quantity=form.quantity.data, reorder_level=form.reorder_level.data, vendor_id=form.vendor_id.data)
        db.session.add(part)
        db.session.commit()
        flash('Spare part saved.', 'success')
        return redirect(url_for('inventory.spare_parts'))
    return render_template('spare_part_form.html', form=form)
