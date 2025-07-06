-- Massa de dados para testes do módulo de Boi Gordo

-- Inserir 50 bovinos
INSERT INTO beef_cattle (official_id, name, birth_date, breed, gender, entry_date, entry_weight, current_weight, target_weight, status, expected_finish_date, notes) VALUES
('BG001', 'Sultão', '2023-01-15', 'Nelore', 'M', '2024-01-10', 380.5, 450.2, 550.0, 'Em Engorda', '2024-12-15', 'Animal saudável, boa conversão alimentar'),
('BG002', 'Trovão', '2023-02-20', 'Angus', 'M', '2024-01-15', 410.0, 470.5, 580.0, 'Em Engorda', '2024-11-20', 'Cruzamento industrial, alto ganho diário'),
('BG003', 'Estrela', '2023-03-10', 'Nelore', 'F', '2024-02-01', 360.0, 410.0, 520.0, 'Em Engorda', '2025-01-10', 'Fêmea para engorda, boa estrutura'),
('BG004', 'Tornado', '2022-11-05', 'Brahman', 'M', '2023-12-10', 420.0, 510.0, 570.0, 'Em Engorda', '2024-10-05', 'Animal de alto desempenho'),
('BG005', 'Relâmpago', '2022-10-12', 'Nelore', 'M', '2023-11-20', 400.0, 520.0, 560.0, 'Vendido', '2024-09-15', 'Vendido antes do prazo por bom desempenho'),
('BG006', 'Tempestade', '2023-04-05', 'Nelore', 'F', '2024-02-10', 370.0, 410.0, 530.0, 'Em Engorda', '2025-01-15', 'Fêmea com bom potencial'),
('BG007', 'Furacão', '2023-01-25', 'Angus', 'M', '2024-01-20', 400.0, 460.0, 570.0, 'Em Engorda', '2024-12-20', 'Animal de boa genética'),
('BG008', 'Raio', '2022-12-10', 'Nelore', 'M', '2023-12-15', 390.0, 470.0, 550.0, 'Em Engorda', '2024-11-15', 'Bom desenvolvimento muscular'),
('BG009', 'Ventania', '2023-02-15', 'Brahman', 'F', '2024-01-25', 350.0, 400.0, 510.0, 'Em Engorda', '2024-12-25', 'Fêmea de porte médio'),
('BG010', 'Ciclone', '2022-11-20', 'Angus', 'M', '2023-12-05', 430.0, 510.0, 580.0, 'Em Engorda', '2024-10-05', 'Animal de alta performance'),
('BG011', 'Tufão', '2022-10-05', 'Nelore', 'M', '2023-11-10', 410.0, 530.0, 570.0, 'Vendido', '2024-09-10', 'Vendido para abate'),
('BG012', 'Avalanche', '2023-03-20', 'Hereford', 'M', '2024-02-05', 390.0, 430.0, 560.0, 'Em Engorda', '2025-01-05', 'Animal de boa estrutura'),
('BG013', 'Nevasca', '2023-01-10', 'Nelore', 'F', '2024-01-05', 360.0, 420.0, 520.0, 'Em Engorda', '2024-12-05', 'Fêmea com bom ganho de peso'),
('BG014', 'Tsunami', '2022-12-15', 'Angus', 'M', '2023-12-20', 420.0, 490.0, 570.0, 'Em Engorda', '2024-11-20', 'Animal de boa conversão alimentar'),
('BG015', 'Vulcão', '2022-11-25', 'Brahman', 'M', '2023-12-01', 440.0, 520.0, 590.0, 'Em Engorda', '2024-10-01', 'Animal de grande porte'),
('BG016', 'Terremoto', '2022-10-15', 'Nelore', 'M', '2023-11-15', 400.0, 510.0, 560.0, 'Vendido', '2024-09-15', 'Vendido para abate'),
('BG017', 'Meteoro', '2023-04-10', 'Angus', 'M', '2024-02-15', 380.0, 420.0, 550.0, 'Em Engorda', '2025-01-15', 'Animal de boa genética'),
('BG018', 'Cometa', '2023-02-05', 'Nelore', 'F', '2024-01-10', 350.0, 410.0, 510.0, 'Em Engorda', '2024-12-10', 'Fêmea com bom potencial'),
('BG019', 'Galáxia', '2022-12-20', 'Hereford', 'F', '2023-12-25', 370.0, 440.0, 530.0, 'Em Engorda', '2024-11-25', 'Fêmea de boa estrutura'),
('BG020', 'Universo', '2022-11-10', 'Angus', 'M', '2023-12-05', 430.0, 510.0, 580.0, 'Em Engorda', '2024-10-05', 'Animal de alta performance'),
('BG021', 'Planeta', '2022-10-20', 'Nelore', 'M', '2023-11-25', 410.0, 520.0, 570.0, 'Vendido', '2024-09-25', 'Vendido para abate'),
('BG022', 'Satélite', '2023-03-15', 'Brahman', 'M', '2024-02-10', 400.0, 440.0, 560.0, 'Em Engorda', '2025-01-10', 'Animal de boa estrutura'),
('BG023', 'Constelação', '2023-01-20', 'Nelore', 'F', '2024-01-15', 360.0, 420.0, 520.0, 'Em Engorda', '2024-12-15', 'Fêmea com bom ganho de peso'),
('BG024', 'Estrela Cadente', '2022-12-25', 'Angus', 'M', '2023-12-30', 420.0, 490.0, 570.0, 'Em Engorda', '2024-11-30', 'Animal de boa conversão alimentar'),
('BG025', 'Via Láctea', '2022-11-15', 'Hereford', 'F', '2023-12-10', 380.0, 450.0, 540.0, 'Em Engorda', '2024-10-10', 'Fêmea de porte médio'),
('BG026', 'Nebulosa', '2022-10-25', 'Nelore', 'M', '2023-11-30', 400.0, 510.0, 560.0, 'Vendido', '2024-09-30', 'Vendido para abate'),
('BG027', 'Buraco Negro', '2023-04-15', 'Angus', 'M', '2024-02-20', 390.0, 430.0, 560.0, 'Em Engorda', '2025-01-20', 'Animal de boa genética'),
('BG028', 'Quasar', '2023-02-10', 'Nelore', 'M', '2024-01-15', 380.0, 440.0, 550.0, 'Em Engorda', '2024-12-15', 'Animal com bom potencial'),
('BG029', 'Pulsar', '2022-12-30', 'Brahman', 'M', '2024-01-05', 410.0, 480.0, 570.0, 'Em Engorda', '2024-11-05', 'Animal de boa estrutura'),
('BG030', 'Supernova', '2022-11-05', 'Angus', 'F', '2023-12-10', 360.0, 430.0, 530.0, 'Em Engorda', '2024-10-10', 'Fêmea de alta performance'),
('BG031', 'Eclipse', '2022-10-10', 'Nelore', 'M', '2023-11-15', 410.0, 520.0, 570.0, 'Vendido', '2024-09-15', 'Vendido para abate'),
('BG032', 'Solstício', '2023-03-25', 'Hereford', 'M', '2024-02-20', 400.0, 440.0, 560.0, 'Em Engorda', '2025-01-20', 'Animal de boa estrutura'),
('BG033', 'Equinócio', '2023-01-15', 'Nelore', 'F', '2024-01-10', 350.0, 410.0, 510.0, 'Em Engorda', '2024-12-10', 'Fêmea com bom ganho de peso'),
('BG034', 'Lua Cheia', '2022-12-20', 'Angus', 'F', '2023-12-25', 370.0, 440.0, 530.0, 'Em Engorda', '2024-11-25', 'Fêmea de boa estrutura'),
('BG035', 'Lua Nova', '2022-11-10', 'Brahman', 'M', '2023-12-15', 430.0, 510.0, 580.0, 'Em Engorda', '2024-10-15', 'Animal de alta performance'),
('BG036', 'Cruzeiro do Sul', '2022-10-15', 'Nelore', 'M', '2023-11-20', 410.0, 520.0, 570.0, 'Vendido', '2024-09-20', 'Vendido para abate'),
('BG037', 'Órion', '2023-04-05', 'Angus', 'M', '2024-02-10', 390.0, 430.0, 560.0, 'Em Engorda', '2025-01-10', 'Animal de boa genética'),
('BG038', 'Andrômeda', '2023-02-15', 'Nelore', 'F', '2024-01-20', 360.0, 420.0, 520.0, 'Em Engorda', '2024-12-20', 'Fêmea com bom potencial'),
('BG039', 'Centauro', '2022-12-25', 'Hereford', 'M', '2023-12-30', 420.0, 490.0, 570.0, 'Em Engorda', '2024-11-30', 'Animal de boa conversão alimentar'),
('BG040', 'Pegasus', '2022-11-20', 'Angus', 'M', '2023-12-25', 440.0, 520.0, 590.0, 'Em Engorda', '2024-10-25', 'Animal de grande porte'),
('BG041', 'Fênix', '2022-10-05', 'Nelore', 'M', '2023-11-10', 400.0, 510.0, 560.0, 'Vendido', '2024-09-10', 'Vendido para abate'),
('BG042', 'Dragão', '2023-03-10', 'Brahman', 'M', '2024-02-15', 410.0, 450.0, 570.0, 'Em Engorda', '2025-01-15', 'Animal de boa estrutura'),
('BG043', 'Hidra', '2023-01-25', 'Nelore', 'F', '2024-01-20', 350.0, 410.0, 510.0, 'Em Engorda', '2024-12-20', 'Fêmea com bom ganho de peso'),
('BG044', 'Leão', '2022-12-15', 'Angus', 'M', '2023-12-20', 420.0, 490.0, 570.0, 'Em Engorda', '2024-11-20', 'Animal de boa conversão alimentar'),
('BG045', 'Touro', '2022-11-25', 'Hereford', 'M', '2023-12-30', 430.0, 510.0, 580.0, 'Em Engorda', '2024-10-30', 'Animal de alta performance'),
('BG046', 'Escorpião', '2022-10-20', 'Nelore', 'M', '2023-11-25', 410.0, 520.0, 570.0, 'Vendido', '2024-09-25', 'Vendido para abate'),
('BG047', 'Sagitário', '2023-04-10', 'Angus', 'M', '2024-02-15', 390.0, 430.0, 560.0, 'Em Engorda', '2025-01-15', 'Animal de boa genética'),
('BG048', 'Capricórnio', '2023-02-05', 'Nelore', 'M', '2024-01-10', 380.0, 440.0, 550.0, 'Em Engorda', '2024-12-10', 'Animal com bom potencial'),
('BG049', 'Aquário', '2022-12-30', 'Brahman', 'F', '2024-01-05', 360.0, 420.0, 520.0, 'Em Engorda', '2024-11-05', 'Fêmea de boa estrutura'),
('BG050', 'Peixes', '2022-11-15', 'Angus', 'F', '2023-12-20', 370.0, 440.0, 530.0, 'Em Engorda', '2024-10-20', 'Fêmea de porte médio');

-- Inserir registros de pesagem para cada bovino (4 registros por bovino)
-- Bovino 1
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(1, '2024-01-10', 380.5, 'Peso de entrada', 1),
(1, '2024-02-10', 400.0, 'Primeiro mês', 1),
(1, '2024-03-10', 420.5, 'Segundo mês', 1),
(1, '2024-04-10', 450.2, 'Terceiro mês', 1);

-- Bovino 2
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(2, '2024-01-15', 410.0, 'Peso de entrada', 1),
(2, '2024-02-15', 430.0, 'Primeiro mês', 1),
(2, '2024-03-15', 450.0, 'Segundo mês', 1),
(2, '2024-04-15', 470.5, 'Terceiro mês', 1);

-- Bovino 3
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(3, '2024-02-01', 360.0, 'Peso de entrada', 2),
(3, '2024-03-01', 380.0, 'Primeiro mês', 2),
(3, '2024-04-01', 410.0, 'Segundo mês', 2);

-- Bovino 4
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(4, '2023-12-10', 420.0, 'Peso de entrada', 2),
(4, '2024-01-10', 450.0, 'Primeiro mês', 2),
(4, '2024-02-10', 480.0, 'Segundo mês', 2),
(4, '2024-03-10', 510.0, 'Terceiro mês', 2);

-- Bovino 5 (vendido)
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(5, '2023-11-20', 400.0, 'Peso de entrada', 1),
(5, '2023-12-20', 430.0, 'Primeiro mês', 1),
(5, '2024-01-20', 460.0, 'Segundo mês', 1),
(5, '2024-02-20', 490.0, 'Terceiro mês', 1),
(5, '2024-03-20', 520.0, 'Quarto mês - Venda', 1);

-- Inserir registros de pesagem para os bovinos restantes (apenas peso de entrada e atual)
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id)
SELECT 
    id, 
    entry_date, 
    entry_weight, 
    'Peso de entrada', 
    1
FROM 
    beef_cattle
WHERE 
    id > 5;

-- Inserir peso atual para bovinos restantes
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id)
SELECT 
    id, 
    DATE_ADD(entry_date, INTERVAL 3 MONTH), 
    current_weight, 
    'Peso atual', 
    1
FROM 
    beef_cattle
WHERE 
    id > 5;

-- Inserir registros de alimentação para os primeiros 5 bovinos
INSERT INTO beef_cattle_feeding (cattle_id, feeding_date, feed_type, quantity, unit, notes, user_id) VALUES
-- Bovino 1
(1, '2024-01-15', 'Ração', 8.0, 'kg', 'Ração de crescimento', 1),
(1, '2024-02-15', 'Ração', 10.0, 'kg', 'Aumento de ração', 1),
(1, '2024-03-15', 'Ração', 12.0, 'kg', 'Ração de engorda', 1),
-- Bovino 2
(2, '2024-01-20', 'Ração', 9.0, 'kg', 'Ração de crescimento', 1),
(2, '2024-02-20', 'Ração', 11.0, 'kg', 'Aumento de ração', 1),
(2, '2024-03-20', 'Ração', 13.0, 'kg', 'Ração de engorda', 1),
-- Bovino 3
(3, '2024-02-05', 'Ração', 7.0, 'kg', 'Ração inicial', 2),
(3, '2024-03-05', 'Ração', 9.0, 'kg', 'Aumento de ração', 2),
-- Bovino 4
(4, '2023-12-15', 'Ração', 9.0, 'kg', 'Ração inicial', 2),
(4, '2024-01-15', 'Ração', 11.0, 'kg', 'Aumento de ração', 2),
(4, '2024-02-15', 'Ração', 13.0, 'kg', 'Ração de engorda', 2),
-- Bovino 5
(5, '2023-11-25', 'Ração', 8.0, 'kg', 'Ração inicial', 1),
(5, '2023-12-25', 'Ração', 10.0, 'kg', 'Aumento de ração', 1),
(5, '2024-01-25', 'Ração', 12.0, 'kg', 'Ração de engorda', 1),
(5, '2024-02-25', 'Ração', 14.0, 'kg', 'Ração final', 1);

-- Inserir registros de alimentação para os bovinos restantes (1 registro por bovino)
INSERT INTO beef_cattle_feeding (cattle_id, feeding_date, feed_type, quantity, unit, notes, user_id)
SELECT 
    id, 
    DATE_ADD(entry_date, INTERVAL 5 DAY), 
    'Ração', 
    ROUND(entry_weight * 0.02, 1), 
    'kg', 
    'Ração inicial', 
    1
FROM 
    beef_cattle
WHERE 
    id > 5;

-- Inserir registros de saúde para os primeiros 5 bovinos
INSERT INTO beef_cattle_health (cattle_id, record_date, record_type, description, medicine, dosage, notes, user_id) VALUES
-- Bovino 1
(1, '2024-01-12', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(1, '2024-02-15', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
-- Bovino 2
(2, '2024-01-17', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(2, '2024-02-20', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
-- Bovino 3
(3, '2024-02-03', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 2),
-- Bovino 4
(4, '2023-12-12', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 2),
(4, '2024-01-15', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 2),
-- Bovino 5
(5, '2023-11-22', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(5, '2023-12-25', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
(5, '2024-01-25', 'Exame', 'Exame de sangue', NULL, NULL, 'Resultados normais', 1);

-- Inserir registros de saúde para os bovinos restantes (vacinação)
INSERT INTO beef_cattle_health (cattle_id, record_date, record_type, description, medicine, dosage, notes, user_id)
SELECT 
    id, 
    DATE_ADD(entry_date, INTERVAL 2 DAY), 
    'Vacinação', 
    'Vacina contra febre aftosa', 
    'Aftovacin', 
    '5ml', 
    'Aplicação subcutânea', 
    1
FROM 
    beef_cattle
WHERE 
    id > 5;

-- Inserir registros de venda para os bovinos vendidos
INSERT INTO beef_cattle_sales (cattle_id, sale_date, final_weight, price_per_kg, total_value, buyer, notes, user_id) VALUES
(5, '2024-03-20', 520.0, 22.50, 11700.00, 'Frigorífico São José', 'Venda antecipada por bom desempenho', 1),
(11, '2024-02-15', 530.0, 22.00, 11660.00, 'Frigorífico São José', 'Venda regular', 1),
(16, '2024-02-20', 510.0, 21.80, 11118.00, 'Frigorífico Boi Gordo', 'Venda regular', 2),
(21, '2024-03-05', 520.0, 22.30, 11596.00, 'Frigorífico São José', 'Venda regular', 1),
(26, '2024-03-10', 510.0, 22.00, 11220.00, 'Frigorífico Boi Gordo', 'Venda regular', 2),
(31, '2024-03-15', 520.0, 22.50, 11700.00, 'Frigorífico São José', 'Venda regular', 1),
(36, '2024-03-25', 520.0, 22.80, 11856.00, 'Frigorífico Boi Gordo', 'Venda regular', 2),
(41, '2024-04-05', 510.0, 23.00, 11730.00, 'Frigorífico São José', 'Venda regular', 1),
(46, '2024-04-10', 520.0, 23.20, 12064.00, 'Frigorífico Boi Gordo', 'Venda regular', 2);