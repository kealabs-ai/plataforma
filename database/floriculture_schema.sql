-- Schema para o módulo de Floricultura
-- Criação das tabelas necessárias para o sistema de gerenciamento de floricultura

-- Tabela de Estufas (Greenhouses)
CREATE TABLE IF NOT EXISTS greenhouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    area_m2 DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50) NOT NULL,
    temperature_control BOOLEAN DEFAULT FALSE,
    humidity_control BOOLEAN DEFAULT FALSE,
    irrigation_system BOOLEAN DEFAULT FALSE,
    location VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de Cultivos de Flores (Flowers)
CREATE TABLE IF NOT EXISTS flower_cultivation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    species VARCHAR(100) NOT NULL,
    variety VARCHAR(100),
    planting_date DATE NOT NULL,
    quantity INT,
    area_m2 DECIMAL(10, 2) NOT NULL,
    greenhouse_id INT,
    expected_harvest_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    notes TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE SET NULL
);

-- Tabela de Fornecedores (Suppliers)
CREATE TABLE IF NOT EXISTS floriculture_suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    products TEXT NOT NULL,
    last_purchase DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para melhorar a performance das consultas
CREATE INDEX idx_flowers_user_id ON flower_cultivations(user_id);
CREATE INDEX idx_flowers_species ON flower_cultivations(species);
CREATE INDEX idx_flowers_status ON flower_cultivations(status);
CREATE INDEX idx_flowers_greenhouse ON flower_cultivations(greenhouse_id);

CREATE INDEX idx_greenhouse_user_id ON greenhouses(user_id);
CREATE INDEX idx_greenhouse_type ON greenhouses(type);

CREATE INDEX idx_suppliers_user_id ON floriculture_suppliers(user_id);
CREATE INDEX idx_suppliers_status ON floriculture_suppliers(status);
CREATE INDEX idx_suppliers_name ON floriculture_suppliers(name);