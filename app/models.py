from datetime import datetime, date, timedelta
from flask_login import UserMixin
from . import db, login_manager

role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True),
)

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Department(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    floor = db.Column(db.String(50))
    building = db.Column(db.String(120))
    locations = db.relationship('Location', backref='department', lazy=True)
    equipment = db.relationship('Equipment', backref='department', lazy=True)

class Location(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    room_number = db.Column(db.String(50), nullable=False)
    bed_number = db.Column(db.String(50))
    equipment = db.relationship('Equipment', backref='location', lazy=True)

class EquipmentCategory(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    maintenance_frequency_days = db.Column(db.Integer, default=90)
    requires_calibration = db.Column(db.Boolean, default=False)
    equipment = db.relationship('Equipment', backref='category', lazy=True)

class Manufacturer(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    website = db.Column(db.String(255))
    equipment = db.relationship('Equipment', backref='manufacturer', lazy=True)

class Role(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles')

class Permission(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class User(UserMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)
    transfers = db.relationship('EquipmentTransfer', backref='transferred_by_user', lazy=True)

    def has_permission(self, code):
        return any(p.code == code for p in self.role.permissions)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Technician(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(50))
    specialization = db.Column(db.String(120))
    certification = db.Column(db.String(255))
    work_orders = db.relationship('WorkOrder', backref='assigned_technician', lazy=True)

class TechnicianCertification(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)
    certificate_name = db.Column(db.String(150), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

class Vendor(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    contact_person = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    spare_parts = db.relationship('SparePart', backref='vendor', lazy=True)
    contracts = db.relationship('ServiceContract', backref='vendor', lazy=True)
    purchase_orders = db.relationship('PurchaseOrder', backref='vendor', lazy=True)

class Equipment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(60), unique=True, nullable=False)
    serial_number = db.Column(db.String(80), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('equipment_category.id'), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
    model_number = db.Column(db.String(120))
    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)
    current_status = db.Column(db.String(50), nullable=False, default='Active')
    criticality_level = db.Column(db.String(50), default='Medium')
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy=True, cascade='all, delete-orphan')
    work_orders = db.relationship('WorkOrder', backref='equipment', lazy=True, cascade='all, delete-orphan')
    pm_schedules = db.relationship('PMSchedule', backref='equipment', lazy=True, cascade='all, delete-orphan')
    calibration_records = db.relationship('CalibrationRecord', backref='equipment', lazy=True, cascade='all, delete-orphan')
    transfers = db.relationship('EquipmentTransfer', backref='equipment', lazy=True, cascade='all, delete-orphan')
    service_contracts = db.relationship('ServiceContract', backref='equipment', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='equipment', lazy=True, cascade='all, delete-orphan')
    compliance_documents = db.relationship('ComplianceDocument', backref='equipment', lazy=True, cascade='all, delete-orphan')

    @property
    def latest_next_due(self):
        dates = [m.next_due_date for m in self.maintenance_records if m.next_due_date]
        return min(dates) if dates else None

class EquipmentTransfer(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    from_location = db.Column(db.String(120), nullable=False)
    to_location = db.Column(db.String(120), nullable=False)
    transfer_date = db.Column(db.DateTime, default=datetime.utcnow)
    transferred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class WorkOrder(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    priority = db.Column(db.String(30), default='Medium')
    status = db.Column(db.String(30), default='Open')
    issue_description = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_to = db.Column(db.Integer, db.ForeignKey('technician.id'))
    completed_date = db.Column(db.DateTime)
    maintenance_records = db.relationship('MaintenanceRecord', backref='work_order', lazy=True)

class MaintenanceRecord(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))
    maintenance_type = db.Column(db.String(50), nullable=False)
    date_performed = db.Column(db.Date, nullable=False)
    findings = db.Column(db.Text)
    actions_taken = db.Column(db.Text)
    cost = db.Column(db.Numeric(10, 2), default=0)
    next_due_date = db.Column(db.Date)
    part_usage = db.relationship('PartUsage', backref='maintenance_record', lazy=True)

class PMSchedule(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    frequency_days = db.Column(db.Integer, nullable=False)
    last_completed = db.Column(db.Date)
    next_due = db.Column(db.Date)

class CalibrationRecord(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    result = db.Column(db.String(80), nullable=False)
    certificate_number = db.Column(db.String(120))
    next_due_date = db.Column(db.Date)

class ServiceContract(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    coverage_type = db.Column(db.String(120), nullable=False)

class SparePart(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    part_number = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=1)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    usages = db.relationship('PartUsage', backref='part', lazy=True)

class PartUsage(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_record.id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('spare_part.id'), nullable=False)
    quantity_used = db.Column(db.Integer, nullable=False)

class PurchaseOrder(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(50), default='Draft')
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy=True, cascade='all, delete-orphan')

class PurchaseOrderItem(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10, 2), default=0)

class AuditLog(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    table_name = db.Column(db.String(120), nullable=False)
    record_id = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)

class ComplianceDocument(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    document_type = db.Column(db.String(120), nullable=False)
    expiry_date = db.Column(db.Date)
    file_url = db.Column(db.String(255))

class Document(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    s3_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(80), nullable=False)
    uploaded_by = db.Column(db.String(120), nullable=False)

class Notification(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(40), default='Unread')


def equipment_overdue_query():
    today = date.today()
    return db.session.query(Equipment).join(MaintenanceRecord).filter(MaintenanceRecord.next_due_date < today).distinct()
