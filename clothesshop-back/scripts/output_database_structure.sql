DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    login VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (login)
);

DROP TABLE IF EXISTS user_personal_info CASCADE;
CREATE TABLE user_personal_info (
    login VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    passport_number VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (login),
    FOREIGN KEY (login) REFERENCES users(login)
);

DROP TABLE IF EXISTS medication_categories CASCADE;
CREATE TABLE medication_categories (
    category VARCHAR(100) NOT NULL,
    higher_category VARCHAR(100) NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (category)
);

DROP TABLE IF EXISTS medications CASCADE;
CREATE TABLE medications (
    medication_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL,
    requires_prescription BOOLEAN NOT NULL,
    delivery_date DATE NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (medication_id),
    FOREIGN KEY (category) REFERENCES medication_categories(category)
);

DROP TABLE IF EXISTS pharmacies CASCADE;
CREATE TABLE pharmacies (
    pharmacy_id BIGINT NOT NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(50) NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (pharmacy_id)
);

DROP TABLE IF EXISTS reviews CASCADE;
CREATE TABLE reviews (
    review_id BIGINT NOT NULL,
    login VARCHAR(100) NOT NULL,
    medication_id BIGINT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT NOT NULL,
    review_date TIMESTAMP NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (review_id),
    FOREIGN KEY (login) REFERENCES users(login),
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);

DROP TABLE IF EXISTS pharmacy_medications CASCADE;
CREATE TABLE pharmacy_medications (
    pharmacy_id BIGINT NOT NULL,
    medication_id BIGINT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (pharmacy_id, medication_id),
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id),
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);

DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    login VARCHAR(100) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (order_id),
    FOREIGN KEY (login) REFERENCES users(login)
);

DROP TABLE IF EXISTS prescriptions CASCADE;
CREATE TABLE prescriptions (
    prescription_id BIGINT NOT NULL,
    login VARCHAR(100) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    issue_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    medication_id BIGINT NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (prescription_id),
    FOREIGN KEY (login) REFERENCES users(login),
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);

DROP TABLE IF EXISTS medication_manufacturers CASCADE;
CREATE TABLE medication_manufacturers (
    manufacturer_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    contact_number VARCHAR(50) NOT NULL,
    contact_email VARCHAR(100) NOT NULL,
    secret VARCHAR(40),
    PRIMARY KEY (manufacturer_name)
);

-- Protection from schema reading
REVOKE ALL ON SCHEMA public FROM public;
REVOKE SELECT ON ALL TABLES IN SCHEMA information_schema FROM public;
REVOKE SELECT ON ALL TABLES IN SCHEMA pg_catalog FROM public;
GRANT USAGE ON SCHEMA public TO public;
