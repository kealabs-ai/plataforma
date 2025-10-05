-- Schema para tabela de plantas ornamentais do módulo de Floricultura

-- Tabela de Plantas Ornamentais
CREATE TABLE IF NOT EXISTS floriculture_plants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL DEFAULT 1,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100),
    category VARCHAR(50) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    sun_needs VARCHAR(50) NOT NULL,
    watering VARCHAR(50) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    image_url TEXT,
    description TEXT,
    care_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de Fornecedores de Floricultura (se não existir)
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

-- Índices para melhorar performance
CREATE INDEX idx_floriculture_plants_user_id ON floriculture_plants(user_id);
CREATE INDEX idx_floriculture_plants_category ON floriculture_plants(category);
CREATE INDEX idx_floriculture_plants_environment ON floriculture_plants(environment);
CREATE INDEX idx_floriculture_plants_name ON floriculture_plants(name);

-- Dados de exemplo para plantas ornamentais
INSERT INTO floriculture_plants (user_id, name, scientific_name, category, environment, sun_needs, watering, stock, price, description, care_instructions) VALUES
(1, 'Rosa Vermelha', 'Rosa gallica', 'Flores', 'Externo', 'Pleno Sol', 'Diária', 25, 15.50, 'Rosa vermelha clássica, perfeita para jardins e arranjos florais.', 'Regar diariamente pela manhã, podar após floração, adubar mensalmente.'),
(1, 'Orquídea Phalaenopsis', 'Phalaenopsis amabilis', 'Flores', 'Interno', 'Meia Sombra', '2-3 dias', 12, 45.00, 'Orquídea elegante de fácil cultivo, ideal para ambientes internos.', 'Regar quando substrato estiver seco, evitar água nas folhas, fertilizar quinzenalmente.'),
(1, 'Lírio Branco', 'Lilium candidum', 'Flores', 'Ambos', 'Meia Sombra', 'Semanal', 18, 22.00, 'Lírio perfumado com flores brancas, excelente para arranjos.', 'Plantar em solo bem drenado, regar moderadamente, proteger do vento forte.'),
(1, 'Violeta Africana', 'Saintpaulia ionantha', 'Flores', 'Interno', 'Sombra', '2-3 dias', 30, 12.00, 'Pequena planta florida ideal para decoração interna.', 'Manter em local com luz indireta, regar por baixo, temperatura entre 18-24°C.'),
(1, 'Samambaia', 'Nephrolepis exaltata', 'Folhagens', 'Interno', 'Sombra', 'Diária', 20, 18.00, 'Samambaia ornamental perfeita para ambientes internos úmidos.', 'Manter solo sempre úmido, borrifar folhas regularmente, evitar sol direto.'),
(1, 'Suculenta Echeveria', 'Echeveria elegans', 'Suculentas', 'Ambos', 'Pleno Sol', 'Semanal', 40, 8.50, 'Suculenta resistente com formato de roseta, fácil manutenção.', 'Regar apenas quando solo estiver seco, necessita boa drenagem, resistente ao calor.'),
(1, 'Antúrio', 'Anthurium andraeanum', 'Flores', 'Interno', 'Meia Sombra', '2-3 dias', 15, 35.00, 'Planta tropical com flores vermelhas duradouras.', 'Manter em ambiente úmido, regar quando solo superficial estiver seco, adubar mensalmente.'),
(1, 'Begônia', 'Begonia semperflorens', 'Flores', 'Ambos', 'Meia Sombra', 'Diária', 25, 10.00, 'Begônia florida com cores vibrantes, ideal para canteiros.', 'Regar regularmente sem encharcar, remover flores murchas, proteger de geadas.');