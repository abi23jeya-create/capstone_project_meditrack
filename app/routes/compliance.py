from flask import Blueprint, render_template
from flask_login import login_required
from ..models import ComplianceDocument, CalibrationRecord, ServiceContract

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/')
@login_required
def overview():
    docs = ComplianceDocument.query.order_by(ComplianceDocument.expiry_date.asc()).all()
    calibrations = CalibrationRecord.query.order_by(CalibrationRecord.next_due_date.asc()).all()
    contracts = ServiceContract.query.order_by(ServiceContract.end_date.asc()).all()
    return render_template('compliance.html', docs=docs, calibrations=calibrations, contracts=contracts)
