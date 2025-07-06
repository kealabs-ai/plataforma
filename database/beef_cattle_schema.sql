-- Esquema de banco de dados para o módulo de Boi Gordo

-- Tabela principal de bovinos para engorda
CREATE TABLE IF NOT EXISTS beef_cattle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    official_id VARCHAR(20) NOT NULL COMMENT 'ID oficial/brinco do animal',
    name VARCHAR(100) COMMENT 'Nome do animal (opcional)',
    birth_date DATE NOT NULL COMMENT 'Data de nascimento',
    breed VARCHAR(50) COMMENT 'Raça do animal',
    gender CHAR(1) NOT NULL COMMENT 'Sexo (M/F)',
    entry_date DATE NOT NULL COMMENT 'Data de entrada no sistema',
    entry_weight DECIMAL(6,1) NOT NULL COMMENT 'Peso de entrada (kg)',
    current_weight DECIMAL(6,1) COMMENT 'Peso atual (kg)',
    target_weight DECIMAL(6,1) COMMENT 'Peso alvo (kg)',
    status VARCHAR(20) NOT NULL DEFAULT 'Em Engorda' COMMENT 'Status (Em Engorda, Vendido, etc)',
    expected_finish_date DATE COMMENT 'Data prevista para término da engorda',
    notes TEXT COMMENT 'Observações',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (official_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Cadastro de bovinos para engorda';

-- Tabela de registros de pesagem
CREATE TABLE IF NOT EXISTS beef_cattle_weights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    weight_date DATE NOT NULL COMMENT 'Data da pesagem',
    weight DECIMAL(6,1) NOT NULL COMMENT 'Peso (kg)',
    notes TEXT COMMENT 'Observações',
    user_id INT COMMENT 'ID do usuário que registrou',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de pesagem dos bovinos';

-- Tabela de registros de alimentação
CREATE TABLE IF NOT EXISTS beef_cattle_feeding (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    feeding_date DATE NOT NULL COMMENT 'Data da alimentação',
    feed_type VARCHAR(50) NOT NULL COMMENT 'Tipo de alimento',
    quantity DECIMAL(6,2) NOT NULL COMMENT 'Quantidade',
    unit VARCHAR(10) NOT NULL COMMENT 'Unidade (kg, g, etc)',
    notes TEXT COMMENT 'Observações',
    user_id INT COMMENT 'ID do usuário que registrou',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de alimentação dos bovinos';

-- Tabela de registros de saúde
CREATE TABLE IF NOT EXISTS beef_cattle_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    record_date DATE NOT NULL COMMENT 'Data do registro',
    record_type VARCHAR(50) NOT NULL COMMENT 'Tipo (Vacinação, Medicação, Exame, etc)',
    description VARCHAR(255) NOT NULL COMMENT 'Descrição do procedimento',
    medicine VARCHAR(100) COMMENT 'Medicamento utilizado',
    dosage VARCHAR(50) COMMENT 'Dosagem',
    notes TEXT COMMENT 'Observações',
    user_id INT COMMENT 'ID do usuário que registrou',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de saúde dos bovinos';

-- Tabela de registros de venda
CREATE TABLE IF NOT EXISTS beef_cattle_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cattle_id INT NOT NULL,
    sale_date DATE NOT NULL COMMENT 'Data da venda',
    final_weight DECIMAL(6,1) NOT NULL COMMENT 'Peso final (kg)',
    price_per_kg DECIMAL(6,2) NOT NULL COMMENT 'Preço por kg (R$)',
    total_value DECIMAL(10,2) NOT NULL COMMENT 'Valor total (R$)',
    buyer VARCHAR(100) COMMENT 'Comprador',
    notes TEXT COMMENT 'Observações',
    user_id INT COMMENT 'ID do usuário que registrou',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cattle_id) REFERENCES beef_cattle(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de venda dos bovinos';

-- Índices para melhorar a performance
CREATE INDEX idx_beef_cattle_status ON beef_cattle(status);
CREATE INDEX idx_beef_cattle_weights_date ON beef_cattle_weights(weight_date);
CREATE INDEX idx_beef_cattle_feeding_date ON beef_cattle_feeding(feeding_date);
CREATE INDEX idx_beef_cattle_health_date ON beef_cattle_health(record_date);
CREATE INDEX idx_beef_cattle_sales_date ON beef_cattle_sales(sale_date);