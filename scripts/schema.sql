CREATE TABLE IF NOT EXISTS department (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL,
  floor VARCHAR(50),
  building VARCHAR(120),
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS location (
  id INT AUTO_INCREMENT PRIMARY KEY,
  department_id INT NOT NULL,
  room_number VARCHAR(50) NOT NULL,
  bed_number VARCHAR(50),
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (department_id) REFERENCES department(id)
);
CREATE TABLE IF NOT EXISTS equipment_category (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL,
  maintenance_frequency_days INT DEFAULT 90,
  requires_calibration BOOLEAN DEFAULT FALSE,
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS manufacturer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) UNIQUE NOT NULL,
  contact_email VARCHAR(120),
  phone VARCHAR(50),
  website VARCHAR(255),
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS role (
  id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(80) UNIQUE NOT NULL,
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS permission (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(80) UNIQUE NOT NULL,
  description VARCHAR(255),
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS vendor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) UNIQUE NOT NULL,
  contact_person VARCHAR(120),
  phone VARCHAR(50),
  email VARCHAR(120),
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS technician (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE,
  phone VARCHAR(50),
  specialization VARCHAR(120),
  certification VARCHAR(255),
  created_at DATETIME,
  updated_at DATETIME
);
CREATE TABLE IF NOT EXISTS user (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  is_active_user BOOLEAN DEFAULT TRUE,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (role_id) REFERENCES role(id)
);
CREATE TABLE IF NOT EXISTS equipment (
  id INT AUTO_INCREMENT PRIMARY KEY,
  asset_tag VARCHAR(60) UNIQUE NOT NULL,
  serial_number VARCHAR(80) UNIQUE NOT NULL,
  category_id INT NOT NULL,
  manufacturer_id INT NOT NULL,
  model_number VARCHAR(120),
  purchase_date DATE,
  warranty_expiry DATE,
  current_status VARCHAR(50) NOT NULL,
  criticality_level VARCHAR(50),
  department_id INT NOT NULL,
  location_id INT NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (category_id) REFERENCES equipment_category(id),
  FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id),
  FOREIGN KEY (department_id) REFERENCES department(id),
  FOREIGN KEY (location_id) REFERENCES location(id)
);
-- Remaining tables are created automatically by SQLAlchemy create_all() in this starter project.
