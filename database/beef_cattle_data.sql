-- Dados de exemplo para Boi Gordo

-- Inserir dados na tabela beef_cattle
INSERT INTO beef_cattle (official_id, name, birth_date, breed, gender, entry_date, entry_weight, current_weight, target_weight, status, expected_finish_date, notes) VALUES
('BG001', 'Sultão', '2023-01-15', 'Nelore', 'M', '2024-01-10', 380.5, 450.2, 550.0, 'Em Engorda', '2024-12-15', 'Animal saudável, boa conversão alimentar'),
('BG002', 'Trovão', '2023-02-20', 'Angus', 'M', '2024-01-15', 410.0, 470.5, 580.0, 'Em Engorda', '2024-11-20', 'Cruzamento industrial, alto ganho diário'),
('BG003', 'Estrela', '2023-03-10', 'Nelore', 'F', '2024-02-01', 360.0, 410.0, 520.0, 'Em Engorda', '2025-01-10', 'Fêmea para engorda, boa estrutura'),
('BG004', 'Tornado', '2022-11-05', 'Brahman', 'M', '2023-12-10', 420.0, 510.0, 570.0, 'Em Engorda', '2024-10-05', 'Animal de alto desempenho'),
('BG005', 'Relâmpago', '2022-10-12', 'Nelore', 'M', '2023-11-20', 400.0, 520.0, 560.0, 'Vendido', '2024-09-15', 'Vendido antes do prazo por bom desempenho');

-- Inserir dados na tabela beef_cattle_weights
INSERT INTO beef_cattle_weights (cattle_id, weight_date, weight, notes, user_id) VALUES
(1, '2024-01-10', 380.5, 'Peso de entrada', 1),
(1, '2024-02-10', 400.0, 'Primeiro mês', 1),
(1, '2024-03-10', 420.5, 'Segundo mês', 1),
(1, '2024-04-10', 450.2, 'Terceiro mês', 1),
(2, '2024-01-15', 410.0, 'Peso de entrada', 1),
(2, '2024-02-15', 430.0, 'Primeiro mês', 1),
(2, '2024-03-15', 450.0, 'Segundo mês', 1),
(2, '2024-04-15', 470.5, 'Terceiro mês', 1),
(3, '2024-02-01', 360.0, 'Peso de entrada', 2),
(3, '2024-03-01', 380.0, 'Primeiro mês', 2),
(3, '2024-04-01', 410.0, 'Segundo mês', 2),
(4, '2023-12-10', 420.0, 'Peso de entrada', 2),
(4, '2024-01-10', 450.0, 'Primeiro mês', 2),
(4, '2024-02-10', 480.0, 'Segundo mês', 2),
(4, '2024-03-10', 510.0, 'Terceiro mês', 2),
(5, '2023-11-20', 400.0, 'Peso de entrada', 1),
(5, '2023-12-20', 430.0, 'Primeiro mês', 1),
(5, '2024-01-20', 460.0, 'Segundo mês', 1),
(5, '2024-02-20', 490.0, 'Terceiro mês', 1),
(5, '2024-03-20', 520.0, 'Quarto mês - Venda', 1);

-- Inserir dados na tabela beef_cattle_feeding
INSERT INTO beef_cattle_feeding (cattle_id, feeding_date, feed_type, quantity, unit, notes, user_id) VALUES
(1, '2024-01-15', 'Ração', 8.0, 'kg', 'Ração de crescimento', 1),
(1, '2024-02-15', 'Ração', 10.0, 'kg', 'Aumento de ração', 1),
(1, '2024-03-15', 'Ração', 12.0, 'kg', 'Ração de engorda', 1),
(2, '2024-01-20', 'Ração', 9.0, 'kg', 'Ração de crescimento', 1),
(2, '2024-02-20', 'Ração', 11.0, 'kg', 'Aumento de ração', 1),
(2, '2024-03-20', 'Ração', 13.0, 'kg', 'Ração de engorda', 1),
(3, '2024-02-05', 'Ração', 7.0, 'kg', 'Ração inicial', 2),
(3, '2024-03-05', 'Ração', 9.0, 'kg', 'Aumento de ração', 2),
(4, '2023-12-15', 'Ração', 9.0, 'kg', 'Ração inicial', 2),
(4, '2024-01-15', 'Ração', 11.0, 'kg', 'Aumento de ração', 2),
(4, '2024-02-15', 'Ração', 13.0, 'kg', 'Ração de engorda', 2),
(5, '2023-11-25', 'Ração', 8.0, 'kg', 'Ração inicial', 1),
(5, '2023-12-25', 'Ração', 10.0, 'kg', 'Aumento de ração', 1),
(5, '2024-01-25', 'Ração', 12.0, 'kg', 'Ração de engorda', 1),
(5, '2024-02-25', 'Ração', 14.0, 'kg', 'Ração final', 1);

-- Inserir dados na tabela beef_cattle_health
INSERT INTO beef_cattle_health (cattle_id, record_date, record_type, description, medicine, dosage, notes, user_id) VALUES
(1, '2024-01-12', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(1, '2024-02-15', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
(2, '2024-01-17', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(2, '2024-02-20', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
(3, '2024-02-03', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 2),
(4, '2023-12-12', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 2),
(4, '2024-01-15', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 2),
(5, '2023-11-22', 'Vacinação', 'Vacina contra febre aftosa', 'Aftovacin', '5ml', 'Aplicação subcutânea', 1),
(5, '2023-12-25', 'Medicação', 'Vermífugo', 'Ivermectina', '10ml', 'Aplicação subcutânea', 1),
(5, '2024-01-25', 'Exame', 'Exame de sangue', NULL, NULL, 'Resultados normais', 1);

-- Inserir dados na tabela beef_cattle_sales
INSERT INTO beef_cattle_sales (cattle_id, sale_date, final_weight, price_per_kg, total_value, buyer, notes, user_id) VALUES
(5, '2024-03-20', 520.0, 22.50, 11700.00, 'Frigorífico São José', 'Venda antecipada por bom desempenho', 1);