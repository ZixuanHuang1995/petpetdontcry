
/* 刊登資料 */
CREATE TABLE published (
  published_id INTEGER PRIMARY KEY AUTOINCREMENT,
  u_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  species TEXT NOT NULL,
  fur TEXT NOT NULL,
  picture TEXT NOT NULL,
  area TEXT NOT NULL,
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sex INTEGER NOT NULL,
  variety TEXT NOT NULL,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  depiction TEXT NOT NULL,
  activate INTEGER NOT NULL,
  published_type INTEGER NOT NULL,
  FOREIGN KEY (u_id) REFERENCES user (u_id)
);

/* 寵物 */
CREATE TABLE pet (
  pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
  u_id INTEGER NOT NULL,
  pet_name TEXT NOT NULL,
  sex INTEGER NOT NULL,
  variety TEXT NOT NULL,
  species TEXT NOT NULL,
  picture TEXT NOT NULL,
  fur TEXT NOT NULL,
  vaccine INTEGER NOT NULL,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (u_id) REFERENCES user (u_id)
);

/* 寵物病歷 */
CREATE TABLE medicalrecord (
  m_id INTEGER PRIMARY KEY AUTOINCREMENT,
  pet_id INTEGER NOT NULL,
  c_id INTEGER NOT NULL,
  disease TEXT NOT NULL,
  doctor TEXT NOT NULL,
  medication TEXT NOT NULL,
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  note TEXT NOT NULL,
  record_type INTEGER NOT NULL,
  FOREIGN KEY (pet_id) REFERENCES pet (pet_id),
  FOREIGN KEY (c_id) REFERENCES clinic (c_id)
);

/* 診所醫生資料 */
CREATE TABLE clinic_doctor (
  c_id INTEGER NOT NULL,
  u_id INTEGER NOT NULL,
  FOREIGN KEY (c_id) REFERENCES clinic (c_id),
  FOREIGN KEY (u_id) REFERENCES user (u_id),
  PRIMARY KEY (c_id, u_id)
);

/* 會員 */
CREATE TABLE user (
  u_id INTEGER PRIMARY KEY AUTOINCREMENT,
  u_name TEXT UNIQUE NOT NULL,
  u_identity TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
  u_password TEXT NOT NULL
);

/* 診所 */
CREATE TABLE clinic (
  c_id INTEGER PRIMARY KEY AUTOINCREMENT,
  c_name TEXT UNIQUE NOT NULL,
  phone TEXT NOT NULL,
  c_address TEXT NOT NULL,
  city TEXT NOT NULL,
  issue_no TEXT NOT NULL,
  issue_date TEXT NOT NULL,
  c_account TEXT NOT NULL,
  c_password TEXT NOT NULL
);

/* 查詢萬用資料 */
CREATE TABLE information (
  i_id INTEGER PRIMARY KEY AUTOINCREMENT,
  i_name TEXT NOT NULL,
  i_function TEXT NOT NULL,
  i_type INTEGER NOT NULL
);