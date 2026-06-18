from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role_id = SelectField('Role', coerce=int)
    submit = SubmitField('Create user')

class EquipmentForm(FlaskForm):
    asset_tag = StringField('Asset Tag', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    manufacturer_id = SelectField('Manufacturer', coerce=int)
    model_number = StringField('Model Number', validators=[Optional()])
    purchase_date = DateField('Purchase Date', validators=[Optional()])
    warranty_expiry = DateField('Warranty Expiry', validators=[Optional()])
    current_status = SelectField('Status', choices=[('Active','Active'),('In Use','In Use'),('Available','Available'),('Under Maintenance','Under Maintenance'),('Out of Service','Out of Service'),('Retired','Retired'),('Lost','Lost')])
    criticality_level = SelectField('Criticality', choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')])
    department_id = SelectField('Department', coerce=int)
    location_id = SelectField('Location', coerce=int)
    submit = SubmitField('Save equipment')

class WorkOrderForm(FlaskForm):
    equipment_id = SelectField('Equipment', coerce=int)
    priority = SelectField('Priority', choices=[('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')])
    status = SelectField('Status', choices=[('Open','Open'),('Assigned','Assigned'),('In Progress','In Progress'),('Completed','Completed'),('Cancelled','Cancelled')])
    issue_description = TextAreaField('Issue Description', validators=[DataRequired()])
    assigned_to = SelectField('Assigned Technician', coerce=int, validators=[Optional()])
    submit = SubmitField('Create work order')

class MaintenanceForm(FlaskForm):
    equipment_id = SelectField('Equipment', coerce=int)
    work_order_id = SelectField('Work Order', coerce=int, validators=[Optional()])
    maintenance_type = SelectField('Maintenance Type', choices=[('Preventive','Preventive'),('Corrective','Corrective'),('Emergency Repair','Emergency Repair'),('Calibration','Calibration'),('Inspection','Inspection')])
    date_performed = DateField('Date Performed', validators=[DataRequired()])
    findings = TextAreaField('Findings')
    actions_taken = TextAreaField('Actions Taken')
    cost = DecimalField('Cost', validators=[Optional(), NumberRange(min=0)])
    next_due_date = DateField('Next Due Date', validators=[Optional()])
    submit = SubmitField('Save maintenance record')

class SparePartForm(FlaskForm):
    name = StringField('Part Name', validators=[DataRequired()])
    part_number = StringField('Part Number', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    reorder_level = IntegerField('Reorder Level', validators=[DataRequired(), NumberRange(min=0)])
    vendor_id = SelectField('Vendor', coerce=int)
    submit = SubmitField('Save spare part')
