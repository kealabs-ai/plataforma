-- Dados para a tabela 'users'
INSERT INTO users (username, password_hash, email, is_active) VALUES
('fazendeiro_joao', 'hashed_pass_123', 'joao.fazendeiro@email.com', TRUE),
('gerente_maria', 'hashed_pass_456', 'maria.gerente@email.com', TRUE),
('supervisor_pedro', 'hashed_pass_789', 'pedro.supervisor@email.com', TRUE);

-- Dados para a tabela 'animals'
INSERT INTO animals (official_id, name, birth_date, breed, gender, status, entry_date) VALUES
('BRL1001', 'Mimosa', '2022-01-15', 'Holandesa', 'F', 'Em Lactação', '2023-01-01'),
('BRL1002', 'Malhada', '2021-06-20', 'Jersey', 'F', 'Em Lactação', '2023-01-01'),
('BRL1003', 'Estrela', '2023-03-01', 'Gir Leiteiro', 'F', 'Seca', '2024-03-01'),
('BRL1004', 'Felicidade', '2022-09-10', 'Holandesa', 'F', 'Em Lactação', '2023-01-01'),
('BRL1005', 'Rainha', '2021-02-05', 'Jersey', 'F', 'Seca', '2023-01-01'),
('BRL1006', 'Sansão', '2020-05-20', 'Nelore', 'M', 'Reprodução', '2023-01-01');

-- Dados para a tabela 'milk_production'
-- Usaremos IDs de animais e usuários que criamos acima.
-- production_date está entre 2024 e 2025 para testes
INSERT INTO milk_production (animal_id, production_date, liters_produced, period, notes, user_id) VALUES
(1, '2024-01-05', 25.5, 'morning', 'Primeira ordenha do dia, boa produção.', 1),
(1, '2024-01-05', 23.0, 'afternoon', 'Segunda ordenha, estável.', 1),
(1, '2024-01-06', 26.0, 'morning', 'Aumento de 0.5 litros.', 1),
(2, '2024-01-05', 20.0, 'morning', 'Produção padrão da Malhada.', 2),
(2, '2024-01-06', 21.0, 'morning', 'Leve aumento.', 2),
(4, '2024-01-07', 28.0, 'morning', 'Excelente produção de Felicidade.', 1),
(4, '2024-01-07', 26.5, 'afternoon', 'Produção da tarde ok.', 1),
(1, '2024-02-10', 24.8, 'morning', 'Produção pós-parto estável.', 1),
(2, '2024-02-10', 20.5, 'morning', 'Manutenção da rotina.', 2),
(4, '2024-02-11', 27.5, 'morning', 'Produção consistente.', 1),
(1, '2025-01-01', 27.0, 'morning', 'Primeira ordenha do ano.', 1),
(1, '2025-01-01', 25.0, 'afternoon', 'Produção de Ano Novo.', 1),
(2, '2025-01-01', 22.0, 'morning', 'Começo de ano produtivo.', 2),
(4, '2025-01-02', 29.0, 'morning', 'Alta produção em 2025.', 1);

-- Dados para a tabela 'logs'
INSERT INTO logs (user_id, action, details) VALUES
(1, 'LOGIN', 'Usuário fazendeiro_joao logou no sistema.'),
(2, 'UPDATE_MILK_PRODUCTION', 'Atualizou registro de produção ID 4.'),
(1, 'CREATE_ANIMAL', 'Animal BRL1006 registrado.'),
(3, 'VIEW_REPORTS', 'Acessou relatório de produção diária.'),
(1, 'LOGOUT', 'Usuário fazendeiro_joao deslogou.'),
(NULL, 'SYSTEM_BOOT', 'Sistema inicializado.'); -- Exemplo de log sem usuário específico


-- Insertion of data based on the image, with English field names
-- 'company_id' and 'user_id' fields are empty in the image, so we'll use NULL or example values.
-- For 'record_date', we'll use the first day of the month and year.
INSERT INTO milk_price_history (company_id, user_id, state, record_date, gross_price_max, net_price_min, net_price_avg, net_price_max, dairy_percentage, rural_producer_pair_price) VALUES
(1, 1, NULL, '2025-01-01', 0.0000, 0.0000, 2.7129, 0.0000, NULL, NULL), -- Adjust 'State', 'Dairy Percentage' and 'Rural Producer Paid Price' if you have more info
(1, 2, NULL, '2025-02-01', 0.0000, 0.0000, 2.8672, 0.0000, NULL, NULL),
(1, 3, NULL, '2025-03-01', 0.0000, 0.0000, 2.9432, 0.0000, NULL, NULL),
(1, 4, NULL, '2025-04-01', 0.0000, 0.0000, 2.8557, 0.0000, NULL, NULL),
(1, 5, NULL, '2025-05-01', 0.0000, 0.0000, 2.7350, 0.0000, NULL, NULL);