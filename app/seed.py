from datetime import date, timedelta
from . import db, bcrypt
from .models import Role, Permission, User, Department, Location, EquipmentCategory, Manufacturer, Vendor, Technician, Equipment, PMSchedule, MaintenanceRecord


def bootstrap_defaults():
    if Role.query.count() == 0:
        permissions = [
            Permission(code='view_dashboard', description='View dashboard'),
            Permission(code='manage_assets', description='Manage equipment and transfers'),
            Permission(code='manage_maintenance', description='Manage work orders and maintenance'),
            Permission(code='manage_inventory', description='Manage spare parts and vendors'),
            Permission(code='manage_procurement', description='Manage purchase orders'),
            Permission(code='view_reports', description='View reports'),
            Permission(code='manage_users', description='Manage users and roles'),
            Permission(code='view_compliance', description='View compliance documents'),
        ]
        db.session.add_all(permissions)
        db.session.flush()

        admin_role = Role(role_name='Admin', permissions=permissions)
        engineer_role = Role(role_name='Biomedical Engineer', permissions=permissions[:-1])
        technician_role = Role(role_name='Technician', permissions=[permissions[0], permissions[2]])
        auditor_role = Role(role_name='Auditor', permissions=[permissions[0], permissions[5], permissions[7]])
        db.session.add_all([admin_role, engineer_role, technician_role, auditor_role])
        db.session.flush()

        admin = User(name='System Admin', email='admin@meditrack.local', password_hash=bcrypt.generate_password_hash('Admin@123').decode('utf-8'), role_id=admin_role.id)
        db.session.add(admin)

    if Department.query.count() == 0:
        icu = Department(name='ICU', floor='1', building='A')
        emergency = Department(name='Emergency', floor='Ground', building='A')
        cardiology = Department(name='Cardiology', floor='2', building='B')
        db.session.add_all([icu, emergency, cardiology])
        db.session.flush()
        db.session.add_all([
            Location(department_id=icu.id, room_number='101', bed_number='1'),
            Location(department_id=icu.id, room_number='102', bed_number='2'),
            Location(department_id=emergency.id, room_number='ER-1', bed_number='A'),
            Location(department_id=cardiology.id, room_number='201', bed_number='3'),
        ])

    if EquipmentCategory.query.count() == 0:
        db.session.add_all([
            EquipmentCategory(name='Ventilator', maintenance_frequency_days=30, requires_calibration=True),
            EquipmentCategory(name='Infusion Pump', maintenance_frequency_days=60, requires_calibration=True),
            EquipmentCategory(name='Defibrillator', maintenance_frequency_days=90, requires_calibration=True),
            EquipmentCategory(name='ECG Monitor', maintenance_frequency_days=120, requires_calibration=False),
        ])

    if Manufacturer.query.count() == 0:
        db.session.add_all([
            Manufacturer(name='Philips', contact_email='support@philips.example', phone='+1-555-0100', website='https://example.com'),
            Manufacturer(name='GE Healthcare', contact_email='support@ge.example', phone='+1-555-0101', website='https://example.com'),
        ])

    if Vendor.query.count() == 0:
        db.session.add_all([
            Vendor(name='MedServe Pvt Ltd', contact_person='Anita Rao', phone='+91-9000000001', email='support@medserve.example'),
            Vendor(name='BioCare Systems', contact_person='Rahul Menon', phone='+91-9000000002', email='service@biocare.example'),
        ])

    if Technician.query.count() == 0:
        db.session.add_all([
            Technician(name='Arjun N', email='arjun@meditrack.local', phone='+91-988000001', specialization='Ventilator Specialist', certification='CBET'),
            Technician(name='Priya S', email='priya@meditrack.local', phone='+91-988000002', specialization='Imaging Equipment Specialist', certification='CBET'),
        ])

    db.session.commit()

    if Equipment.query.count() == 0:
        category = EquipmentCategory.query.first()
        manufacturer = Manufacturer.query.first()
        dept = Department.query.first()
        location = Location.query.first()
        equipment = Equipment(
            asset_tag='MED-1001',
            serial_number='VN-AX1001',
            category_id=category.id,
            manufacturer_id=manufacturer.id,
            model_number='VX-900',
            purchase_date=date.today() - timedelta(days=400),
            warranty_expiry=date.today() + timedelta(days=200),
            current_status='In Use',
            criticality_level='Critical',
            department_id=dept.id,
            location_id=location.id,
        )
        db.session.add(equipment)
        db.session.flush()
        db.session.add(PMSchedule(equipment_id=equipment.id, frequency_days=30, last_completed=date.today()-timedelta(days=40), next_due=date.today()-timedelta(days=10)))
        db.session.add(MaintenanceRecord(equipment_id=equipment.id, maintenance_type='Preventive', date_performed=date.today()-timedelta(days=40), findings='Routine maintenance complete.', actions_taken='Replaced filter and validated settings.', cost=1500, next_due_date=date.today()-timedelta(days=10)))
        db.session.commit()
