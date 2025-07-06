-- Migration: Add Beef Cattle tables

-- Tabela de Boi Gordo (Beef Cattle)
CREATE TABLE IF NOT EXISTS beef_cattle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    official_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100),
    birth_date DATE NOT NULL,
    breed VARCHAR(100),
    gender CHAR(1) NOT NULL,
    entry_date DATE NOT NULL,
    entry_weight DECIMAL(8,2) NOT NULL,
    current_weight DECIMAL(8,2),
    target_weight DECIMAL(8,2),
    status VARCHAR(50) DEFAULT 'Em Engorda',
    expected_finish_date DATE,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Pesagens (Weight Records)
CREATE TABLE IF NOT EXISTS beef_cattle_weights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    weight_date DATE NOT NULL,
    weight DECIMAL(8,2) NOT NULL,
    notes TEXT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabela de Alimentação (Feeding Records)
CREATE TABLE IF NOT EXISTS beef_cattle_feeding (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    feeding_date DATE NOT NULL,
    feed_type VARCHAR(100) NOT NULL,
    quantity DECIMAL(8,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    notes TEXT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabela de Saúde (Health Records)
CREATE TABLE IF NOT EXISTS beef_cattle_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    record_date DATE NOT NULL,
    record_type ENUM('Vacinação', 'Medicação', 'Exame', 'Outro') NOT NULL,
    description VARCHAR(255) NOT NULL,
    medicine VARCHAR(100),
    dosage VARCHAR(50),
    notes TEXT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabela de Venda/Abate (Sale/Slaughter Records)
CREATE TABLE IF NOT EXISTS beef_cattle_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    sale_date DATE NOT NULL,
    final_weight DECIMAL(8,2) NOT NULL,
    price_per_kg DECIMAL(10,2) NOT NULL,
    total_value DECIMAL(12,2) NOT NULL,
    buyer VARCHAR(100),
    notes TEXT,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Índices para performance
CREATE INDEX idx_beef_cattle_status ON beef_cattle(status);
CREATE INDEX idx_beef_cattle_weights_date ON beef_cattle_weights(weight_date);
CREATE INDEX idx_beef_cattle_feeding_date ON beef_cattle_feeding(feeding_date);
CREATE INDEX idx_beef_cattle_health_date ON beef_cattle_health(record_date);
CREATE INDEX idx_beef_cattle_sales_date ON beef_cattle_sales(sale_date);