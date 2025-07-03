-- Tabela de Animais
CREATE TABLE animals (
    animal_id INT AUTO_INCREMENT PRIMARY KEY,
    official_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100),
    birth_date DATE NOT NULL,
    breed VARCHAR(100),
    gender CHAR(1) NOT NULL,
    status VARCHAR(50),
    entry_date DATE
);

-- Tabela de Produção de Leite
CREATE TABLE milk_production (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    production_date DATE NOT NULL,
    liters_produced FLOAT NOT NULL,
    period VARCHAR(20) NOT NULL,
    notes TEXT,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id)
);

-- Índices para performance (opcional)
CREATE INDEX idx_animals_status ON animals(status);
CREATE INDEX idx_milk_production_date ON milk_production(production_date);
CREATE INDEX idx_milk_production_animal_id ON milk_production(animal_id);

-- Exemplo de tabela de usuários (caso use autenticação)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Exemplo de tabela de logs (opcional)
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE milk_production
ADD COLUMN user_id INT,
ADD CONSTRAINT fk_milk_user FOREIGN KEY (user_id) REFERENCES users(id);