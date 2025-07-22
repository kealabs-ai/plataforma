-- Esquema de banco de dados para os módulos de Floricultura e Paisagismo
-- Compatível com MySQL 5.7.44

-- =============================
-- Tabelas para Floricultura
-- =============================

-- Tabela para registro de estufas (precisa ser criada primeiro devido às referências)
CREATE TABLE IF NOT EXISTS greenhouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    area_m2 FLOAT NOT NULL,
    type VARCHAR(50) NOT NULL,
    temperature_control TINYINT(1) DEFAULT 0,
    humidity_control TINYINT(1) DEFAULT 0,
    irrigation_system TINYINT(1) DEFAULT 0,
    location VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de cultivo de flores
CREATE TABLE IF NOT EXISTS flower_cultivation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    species VARCHAR(100) NOT NULL,
    variety VARCHAR(100) NOT NULL,
    planting_date DATE NOT NULL,
    quantity INT NOT NULL,
    area_m2 FLOAT NOT NULL,
    greenhouse_id INT,
    expected_harvest_date DATE,
    status VARCHAR(50) DEFAULT 'Em Cultivo',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE SET NULL
);

-- Tabela para registro de clima nas estufas
CREATE TABLE IF NOT EXISTS greenhouse_climate_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    greenhouse_id INT NOT NULL,
    user_id INT NOT NULL,
    record_date DATE NOT NULL,
    record_time VARCHAR(5) NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    light_level FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (greenhouse_id) REFERENCES greenhouses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de colheitas
CREATE TABLE IF NOT EXISTS flower_harvest_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flower_id INT NOT NULL,
    user_id INT NOT NULL,
    harvest_date DATE NOT NULL,
    quantity INT NOT NULL,
    quality_grade VARCHAR(10) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flower_id) REFERENCES flower_cultivation(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de tratamentos (fertilização, irrigação, etc.)
CREATE TABLE IF NOT EXISTS flower_treatment_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flower_id INT NOT NULL,
    user_id INT NOT NULL,
    treatment_date DATE NOT NULL,
    treatment_type VARCHAR(50) NOT NULL,
    product_used VARCHAR(100) NOT NULL,
    quantity FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flower_id) REFERENCES flower_cultivation(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de vendas de flores
CREATE TABLE IF NOT EXISTS flower_sale_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flower_id INT NOT NULL,
    user_id INT NOT NULL,
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    price_per_unit FLOAT NOT NULL,
    total_value FLOAT NOT NULL,
    buyer VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flower_id) REFERENCES flower_cultivation(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para preferências do usuário relacionadas à floricultura
-- Usando TEXT em vez de JSON para compatibilidade
CREATE TABLE IF NOT EXISTS user_floriculture_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preferred_flowers TEXT COMMENT 'JSON serializado como string',
    preferred_notification_method VARCHAR(50) DEFAULT 'email',
    notification_frequency VARCHAR(50) DEFAULT 'daily',
    dashboard_layout TEXT COMMENT 'JSON serializado como string',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para atividades do usuário relacionadas à floricultura
CREATE TABLE IF NOT EXISTS user_floriculture_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT COMMENT 'JSON serializado como string',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para notificações do usuário relacionadas à floricultura
CREATE TABLE IF NOT EXISTS user_floriculture_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    related_entity_type VARCHAR(50),
    related_entity_id INT,
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =============================
-- Tabelas para Paisagismo
-- =============================

-- Tabela para projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    client_name VARCHAR(100) NOT NULL,
    project_type VARCHAR(50) NOT NULL,
    area_m2 FLOAT NOT NULL,
    start_date DATE NOT NULL,
    expected_end_date DATE,
    budget FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Em Andamento',
    address TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para tarefas de projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'Pendente',
    assigned_to VARCHAR(100),
    priority VARCHAR(50) DEFAULT 'Média',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para materiais de projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    unit_price FLOAT NOT NULL,
    supplier VARCHAR(100),
    purchase_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de plantio em projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_planting_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    planting_date DATE NOT NULL,
    plant_type VARCHAR(50) NOT NULL,
    species VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    area_m2 FLOAT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de manutenção em projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_maintenance_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    maintenance_date DATE NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    hours_spent FLOAT NOT NULL,
    materials_used TEXT,
    cost FLOAT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para registro de despesas em projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_expense_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    expense_date DATE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    supplier VARCHAR(100),
    invoice_number VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para fotos de projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_project_photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    photo_date DATE NOT NULL,
    photo_url VARCHAR(255) NOT NULL,
    description TEXT,
    is_before_photo TINYINT(1) DEFAULT 0,
    is_after_photo TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela para feedback de clientes em projetos de paisagismo
CREATE TABLE IF NOT EXISTS landscaping_client_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    feedback_date DATE NOT NULL,
    rating INT NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES landscaping_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Inserir dados de exemplo para Floricultura

-- Usuários (assumindo que a tabela users já existe)
INSERT INTO users (id, username, email, password_hash, full_name, role, created_at)
VALUES 
(1, 'joao_silva', 'joao@example.com', 'hash_password', 'João Silva', 'admin', NOW()),
(2, 'maria_santos', 'maria@example.com', 'hash_password', 'Maria Santos', 'user', NOW())
ON DUPLICATE KEY UPDATE id=id;

-- Estufas
INSERT INTO greenhouses (user_id, name, area_m2, type, temperature_control, humidity_control, irrigation_system, location, notes)
VALUES 
(1, 'Estufa Principal', 500.0, 'Vidro', 1, 1, 1, 'Setor Norte', 'Estufa para flores delicadas'),
(1, 'Estufa Secundária', 300.0, 'Plástico', 0, 1, 1, 'Setor Sul', 'Estufa para mudas'),
(1, 'Estufa Experimental', 150.0, 'Policarbonato', 1, 1, 1, 'Setor Leste', 'Estufa para testes de novas variedades');

-- Cultivos de flores
INSERT INTO flower_cultivation (user_id, species, variety, planting_date, quantity, area_m2, greenhouse_id, expected_harvest_date, status, notes)
VALUES 
(1, 'Rosa', 'Híbrida de Chá', '2024-03-15', 500, 100.0, 1, '2024-06-15', 'Em Cultivo', 'Crescimento saudável'),
(1, 'Tulipa', 'Darwin Híbrida', '2024-02-10', 1000, 150.0, 2, '2024-05-10', 'Em Cultivo', 'Irrigação diária necessária'),
(1, 'Orquídea', 'Phalaenopsis', '2024-01-05', 300, 75.0, 3, '2024-07-05', 'Em Cultivo', 'Ambiente controlado');

-- Registros de clima
INSERT INTO greenhouse_climate_records (greenhouse_id, user_id, record_date, record_time, temperature, humidity, light_level, notes)
VALUES 
(1, 1, '2024-04-10', '08:00', 22.5, 75.0, 800.0, 'Manhã ensolarada'),
(1, 1, '2024-04-10', '14:00', 26.8, 65.0, 1200.0, 'Pico de temperatura diária'),
(1, 1, '2024-04-10', '20:00', 21.0, 80.0, 100.0, 'Noite');

-- Registros de colheita
INSERT INTO flower_harvest_records (flower_id, user_id, harvest_date, quantity, quality_grade, notes)
VALUES 
(1, 1, '2024-06-15', 200, 'A', 'Excelente qualidade'),
(1, 1, '2024-06-16', 150, 'B', 'Qualidade média');

-- Registros de tratamento
INSERT INTO flower_treatment_records (flower_id, user_id, treatment_date, treatment_type, product_used, quantity, unit, notes)
VALUES 
(1, 1, '2024-04-10', 'Fertilização', 'NPK 10-10-10', 5.0, 'kg', 'Aplicação uniforme'),
(1, 1, '2024-04-15', 'Irrigação', 'Água', 500.0, 'L', 'Irrigação por gotejamento'),
(1, 1, '2024-04-20', 'Controle de Pragas', 'Inseticida Orgânico', 2.0, 'L', 'Aplicação preventiva');

-- Registros de venda
INSERT INTO flower_sale_records (flower_id, user_id, sale_date, quantity, price_per_unit, total_value, buyer, notes)
VALUES 
(1, 1, '2024-06-20', 150, 5.0, 750.0, 'Floricultura Primavera', 'Entrega no local'),
(1, 1, '2024-06-25', 50, 5.0, 250.0, 'Decorações Flor de Lis', 'Pagamento à vista');

-- Preferências do usuário (usando JSON serializado como string)
INSERT INTO user_floriculture_preferences (user_id, preferred_flowers, preferred_notification_method, notification_frequency, dashboard_layout)
VALUES 
(1, '["Rosa", "Orquídea", "Tulipa"]', 'email', 'daily', '{"charts_order": ["species", "harvest", "sales", "quality"], "show_upcoming_harvests": true, "show_recent_sales": true}');

-- Atividades do usuário
INSERT INTO user_floriculture_activities (user_id, activity_type, activity_id, timestamp, details)
VALUES 
(1, 'cultivation', 1, '2024-03-15 10:00:00', '{"action": "create", "species": "Rosa", "variety": "Híbrida de Chá", "quantity": 500}'),
(1, 'harvest', 1, '2024-06-15 09:30:00', '{"action": "create", "flower_id": 1, "quantity": 200, "quality_grade": "A"}');

-- Notificações do usuário
INSERT INTO user_floriculture_notifications (user_id, title, message, notification_type, related_entity_type, related_entity_id, is_read, created_at)
VALUES 
(1, 'Colheita Próxima', 'A colheita de Rosas está programada para os próximos 7 dias.', 'reminder', 'flower', 1, 0, '2024-06-08 08:00:00'),
(1, 'Alerta de Temperatura', 'A temperatura na Estufa Principal está acima do ideal (28°C).', 'alert', 'greenhouse', 1, 1, '2024-06-07 14:30:00');

-- Inserir dados de exemplo para Paisagismo

-- Projetos de paisagismo
INSERT INTO landscaping_projects (user_id, name, client_name, project_type, area_m2, start_date, expected_end_date, budget, status, address, description)
VALUES 
(1, 'Jardim Residencial Silva', 'João Silva', 'Residencial', 250.0, '2024-03-10', '2024-05-15', 15000.0, 'Em Andamento', 'Rua das Flores, 123', 'Projeto de jardim residencial com área de lazer'),
(1, 'Praça Central', 'Prefeitura Municipal', 'Público', 1200.0, '2024-02-05', '2024-06-30', 75000.0, 'Em Andamento', 'Av. Principal, s/n', 'Revitalização da praça central');

-- Tarefas de projetos
INSERT INTO landscaping_tasks (project_id, user_id, task_name, description, start_date, end_date, status, assigned_to, priority)
VALUES 
(1, 1, 'Preparação do terreno', 'Limpeza e nivelamento do terreno', '2024-03-15', '2024-03-20', 'Concluída', 'Equipe de Preparação', 'Alta'),
(1, 1, 'Plantio de árvores', 'Plantio de árvores conforme projeto', '2024-03-22', NULL, 'Em Andamento', 'Equipe de Plantio', 'Média');

-- Materiais de projetos
INSERT INTO landscaping_materials (project_id, user_id, name, category, quantity, unit, unit_price, supplier, purchase_date, notes)
VALUES 
(1, 1, 'Muda de Ipê Amarelo', 'Plantas', 10, 'unidade', 45.0, 'Viveiro Flora Nativa', '2024-03-12', 'Mudas de 1,5m de altura'),
(1, 1, 'Terra adubada', 'Materiais de Construção', 5, 'm³', 120.0, 'Materiais de Construção XYZ', '2024-03-14', 'Terra adubada para plantio');

-- Registros de plantio
INSERT INTO landscaping_planting_records (project_id, user_id, planting_date, plant_type, species, quantity, area_m2, notes)
VALUES 
(1, 1, '2024-03-25', 'Árvore', 'Ipê Amarelo', 3, 30.0, 'Plantio em área sombreada'),
(1, 1, '2024-03-26', 'Arbusto', 'Azaleia', 15, 20.0, 'Plantio em canteiros frontais');

-- Registros de manutenção
INSERT INTO landscaping_maintenance_records (project_id, user_id, maintenance_date, maintenance_type, description, hours_spent, materials_used, cost, notes)
VALUES 
(1, 1, '2024-04-10', 'Poda', 'Poda de formação em arbustos', 4.5, 'Tesoura de poda, luvas', 350.0, 'Realizado conforme planejado'),
(1, 1, '2024-04-15', 'Irrigação', 'Irrigação completa do jardim', 2.0, 'Sistema de irrigação automático', 150.0, 'Ajuste no sistema para economia de água');

-- Registros de despesas
INSERT INTO landscaping_expense_records (project_id, user_id, expense_date, description, category, amount, supplier, invoice_number, notes)
VALUES 
(1, 1, '2024-03-12', 'Compra de mudas', 'Materiais', 2500.0, 'Viveiro Flora Nativa', 'NF-12345', 'Mudas de árvores e arbustos'),
(1, 1, '2024-03-14', 'Contratação de equipe de plantio', 'Mão de obra', 3500.0, 'Serviços de Jardinagem Ltda', 'NF-54321', 'Equipe de 5 pessoas por 2 dias');

-- Fotos de projetos
INSERT INTO landscaping_project_photos (project_id, user_id, photo_date, photo_url, description, is_before_photo, is_after_photo)
VALUES 
(1, 1, '2024-03-10', '/uploads/projects/1/before_1.jpg', 'Terreno antes do início do projeto', 1, 0),
(1, 1, '2024-03-25', '/uploads/projects/1/progress_1.jpg', 'Após preparação do terreno', 0, 0);

-- Feedback de clientes
INSERT INTO landscaping_client_feedback (project_id, user_id, feedback_date, rating, comments)
VALUES 
(1, 1, '2024-04-01', 5, 'Muito satisfeito com o andamento do projeto até o momento.');