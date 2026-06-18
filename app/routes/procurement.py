from flask import Blueprint, render_template
from flask_login import login_required
from ..models import PurchaseOrder

procurement_bp = Blueprint('procurement', __name__)

@procurement_bp.route('/purchase-orders')
@login_required
def purchase_orders():
    orders = PurchaseOrder.query.order_by(PurchaseOrder.date.desc()).all()
    return render_template('purchase_orders.html', orders=orders)
