-- Usuários
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Talhões
CREATE TABLE plots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(50),
    area_ha DECIMAL(10,2),
    climate VARCHAR(50),
    recommended_crop VARCHAR(100),
    soil_type VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Análises de solo
CREATE TABLE soil_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plot_id INT NOT NULL,
    analysis_date DATE NOT NULL,
    pH DECIMAL(4,2),
    nitrogen DECIMAL(6,2),
    phosphorus DECIMAL(6,2),
    potassium DECIMAL(6,2),
    organic_matter DECIMAL(6,2),
    recommendation TEXT,
    FOREIGN KEY (plot_id) REFERENCES plots(id)
);

-- Produção agrícola
CREATE TABLE productions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plot_id INT NOT NULL,
    crop VARCHAR(50) NOT NULL,
    area_ha DECIMAL(10,2) NOT NULL,
    production_kg DECIMAL(12,2),
    harvest_date DATE,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (plot_id) REFERENCES plots(id)
);

-- Insumos
CREATE TABLE inputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    purchase_date DATE,
    supplier VARCHAR(100),
    product VARCHAR(100),
    quantity DECIMAL(10,2),
    unit VARCHAR(10),
    total_cost DECIMAL(12,2),
    purpose TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Atividades no campo
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plot_id INT NOT NULL,
    activity_date DATE,
    description VARCHAR(255),
    responsible VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (plot_id) REFERENCES plots(id)
);

-- Financeiro
CREATE TABLE finances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    entry_date DATE,
    type ENUM('Receita', 'Despesa') NOT NULL,
    description VARCHAR(255),
    value DECIMAL(12,2),
    category VARCHAR(100),
    payment_method VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Recomendação de culturas
CREATE TABLE crop_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    climate VARCHAR(50) NOT NULL,
    min_area DECIMAL(10,2) NOT NULL,
    max_area DECIMAL(10,2) NOT NULL,
    recommended_crop VARCHAR(100) NOT NULL,
    description TEXT
);

-- Laticínios
CREATE TABLE dairies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    contact_info TEXT
);

-- Relacionamento usuário <-> laticínio
CREATE TABLE user_dairies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    dairy_id INT NOT NULL,
    start_date DATE,
    active TINYINT(1) DEFAULT 1,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (dairy_id) REFERENCES dairies(id)
);

-- Produção de leite
CREATE TABLE milk_production (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    production_date DATE NOT NULL,
    liters_produced DECIMAL(10,2),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Criação da tabela de animais
CREATE TABLE animals (
    -- ID único do animal, chave primária
    animal_id INT PRIMARY KEY AUTO_INCREMENT,
    
    -- Número de identificação (ex: brinco), obrigatório e único
    official_id VARCHAR(50) NOT NULL UNIQUE,
    
    -- Nome do animal
    name VARCHAR(100),
    
    -- Data de nascimento do animal, obrigatório
    birth_date DATE NOT NULL,
    
    -- Raça do animal
    breed VARCHAR(100),
    
    -- Sexo do animal (F para fêmea, M para macho)
    gender CHAR(1) NOT NULL,
    
    -- Status do animal (ex: Em Lactação, Seca, Bezerra)
    status VARCHAR(50),
    
    -- Data de entrada no rebanho, usando a sintaxe corrigida para MySQL
    entry_date timestamp
);

-- Adição de um índice para otimizar buscas por ID
CREATE INDEX idx_official_id ON animals(official_id);