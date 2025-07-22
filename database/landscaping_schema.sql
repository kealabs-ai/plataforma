-- Schema para o módulo de Paisagismo
-- Criação das tabelas necessárias para o sistema de gerenciamento de paisagismo

-- Important: For MySQL 5.4.77, the `users` table needs to exist
-- or be created before these tables if it's referenced by foreign keys.
-- Assuming 'users' table structure:
-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(50) NOT NULL UNIQUE,
--     email VARCHAR(100) NOT NULL UNIQUE,
--     -- Add other user-related fields as needed
-- );


-- Tabela de Clientes CRM
-- Renamed to landscaping_clients for consistency with foreign keys
CREATE TABLE IF NOT EXISTS landscaping_crm_clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL, -- Assuming a user manages clients
    client_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(50),
    address VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    client_type VARCHAR(50), -- Ex: 'Residencial', 'Comercial', 'Público'
    industry VARCHAR(100),   -- Ex: 'Paisagismo', 'Construção', etc.
    status VARCHAR(50) DEFAULT 'Lead', -- Ex: 'Lead', 'Qualificado', 'Ativo', 'Inativo', 'Perdido'
    last_interaction_date DATE,
    next_follow_up_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8; -- InnoDB for transactional integrity and foreign keys

---

-- Tabela de Projetos de Paisagismo
CREATE TABLE IF NOT EXISTS landscaping_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    client_id INT NOT NULL, -- Added client_id for direct client association
    name VARCHAR(100) NOT NULL,
    project_type VARCHAR(50),
    area_m2 DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(12, 2),
    status VARCHAR(50) NOT NULL DEFAULT 'planejamento',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES landscaping_clients(id) ON DELETE RESTRICT -- Prevent deleting client if projects exist
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

---

-- Tabela de Fornecedores de Paisagismo
CREATE TABLE IF NOT EXISTS landscaping_suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100), -- Made nullable
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE, -- Added UNIQUE constraint for email
    products TEXT NOT NULL,
    last_contract DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

---

-- Tabela de Serviços de Paisagismo
-- Consolidated into one 'landscaping_services' table as per common structure
CREATE TABLE IF NOT EXISTS landscaping_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    average_duration DECIMAL(5, 2), -- Made nullable
    base_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    image_url VARCHAR(500), -- Made nullable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

---

-- Tabela de Orçamentos (Quotes)
-- Corrected foreign key reference from landscaping_clients
CREATE TABLE IF NOT EXISTS landscaping_quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Added user_id for owner of the quote
    client_id INT NOT NULL,
    project_id INT, -- Optional: Link quote to a project
    description TEXT, -- Made nullable, can be derived from items
    valid_until DATE NOT NULL,
    discount DECIMAL(5,2) DEFAULT 0,
    total_value DECIMAL(12,2) NOT NULL,
    notes TEXT,
    status VARCHAR(32) DEFAULT 'Pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Added updated_at
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES landscaping_clients(id) ON DELETE RESTRICT,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

---

-- Tabela de Itens de Orçamento (Quote Items)
-- This table was duplicated, consolidated and corrected
CREATE TABLE IF NOT EXISTS landscaping_quote_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote_id INT NOT NULL,
    service_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL, -- Calculated field
    description TEXT, -- Specific description for this item in the quote
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (quote_id) REFERENCES landscaping_quotes(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES landscaping_services(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

---

-- Tabela de Manutenção de Paisagismo
CREATE TABLE IF NOT EXISTS landscaping_maintenance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT NOT NULL,
    maintenance_date DATE NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    cost DECIMAL(10, 2),
    duration_hours DECIMAL(5, 2),
    status VARCHAR(50) NOT NULL DEFAULT 'concluído',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


---

-- Indexing for Performance Tuning

-- Here's a refined set of indexes to improve query performance on your tables.

-- sql
-- Índices para melhorar a performance das consultas

-- landscaping_clients
CREATE INDEX idx_clients_user_id ON landscaping_clients(user_id);
CREATE INDEX idx_clients_name ON landscaping_clients(client_name);
CREATE INDEX idx_clients_email ON landscaping_clients(email); -- Useful for searches
CREATE INDEX idx_clients_status ON landscaping_clients(status);

-- landscaping_projects
CREATE INDEX idx_projects_user_id ON landscaping_projects(user_id);
CREATE INDEX idx_projects_client_id ON landscaping_projects(client_id);
CREATE INDEX idx_projects_status ON landscaping_projects(status);
CREATE INDEX idx_projects_start_date ON landscaping_projects(start_date); -- For date range queries

-- landscaping_suppliers
CREATE INDEX idx_suppliers_user_id ON landscaping_suppliers(user_id);
CREATE INDEX idx_suppliers_name ON landscaping_suppliers(name);
CREATE INDEX idx_suppliers_status ON landscaping_suppliers(status);

-- landscaping_services
CREATE INDEX idx_services_user_id ON landscaping_services(user_id);
CREATE INDEX idx_services_category ON landscaping_services(category);
CREATE INDEX idx_services_status ON landscaping_services(status);
CREATE INDEX idx_services_name ON landscaping_services(service_name);

-- landscaping_quotes
CREATE INDEX idx_quotes_user_id ON landscaping_quotes(user_id);
CREATE INDEX idx_quotes_client_id ON landscaping_quotes(client_id);
CREATE INDEX idx_quotes_status ON landscaping_quotes(status);
CREATE INDEX idx_quotes_valid_until ON landscaping_quotes(valid_until);

-- landscaping_quote_items
CREATE INDEX idx_quote_items_quote_id ON landscaping_quote_items(quote_id);
CREATE INDEX idx_quote_items_service_id ON landscaping_quote_items(service_id);

-- landscaping_maintenance
CREATE INDEX idx_maintenance_user_id ON landscaping_maintenance(user_id);
CREATE INDEX idx_maintenance_project_id ON landscaping_maintenance(project_id);
CREATE INDEX idx_maintenance_date ON landscaping_maintenance(date);
CREATE INDEX idx_maintenance_type ON landscaping_maintenance(type);
CREATE INDEX idx_maintenance_status ON landscaping_maintenance(status);