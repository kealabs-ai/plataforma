-- Queries para o módulo de Paisagismo
-- Consultas SQL para operações CRUD nas tabelas de paisagismo

-- OPERAÇÕES PARA PROJETOS DE PAISAGISMO

-- Criar um novo projeto de paisagismo
INSERT INTO landscaping_projects (
    user_id, name, client_name, area_m2, location, 
    start_date, end_date, budget, status, description
) VALUES (
    :user_id, :name, :client_name, :area_m2, :location, 
    :start_date, :end_date, :budget, :status, :description
);

-- Obter todos os projetos de paisagismo com filtros e paginação
SELECT * FROM landscaping_projects 
WHERE user_id = :user_id
    AND (:status IS NULL OR status = :status)
    AND (:client_name IS NULL OR client_name LIKE CONCAT('%', :client_name, '%'))
ORDER BY start_date DESC
LIMIT :limit OFFSET :offset;

-- Contar total de projetos de paisagismo com filtros
SELECT COUNT(*) FROM landscaping_projects 
WHERE user_id = :user_id
    AND (:status IS NULL OR status = :status)
    AND (:client_name IS NULL OR client_name LIKE CONCAT('%', :client_name, '%'));

-- Obter um projeto de paisagismo específico
SELECT * FROM landscaping_projects 
WHERE id = :project_id;

-- Atualizar um projeto de paisagismo
UPDATE landscaping_projects
SET 
    name = COALESCE(:name, name),
    client_name = COALESCE(:client_name, client_name),
    area_m2 = COALESCE(:area_m2, area_m2),
    location = COALESCE(:location, location),
    start_date = COALESCE(:start_date, start_date),
    end_date = COALESCE(:end_date, end_date),
    budget = COALESCE(:budget, budget),
    status = COALESCE(:status, status),
    description = COALESCE(:description, description)
WHERE id = :project_id AND user_id = :user_id;

-- Excluir um projeto de paisagismo
DELETE FROM landscaping_projects 
WHERE id = :project_id AND user_id = :user_id;

-- OPERAÇÕES PARA MANUTENÇÃO DE PAISAGISMO

-- Criar um novo registro de manutenção
INSERT INTO landscaping_maintenance (
    user_id, project_id, date, type, description, 
    cost, duration_hours, status, notes
) VALUES (
    :user_id, :project_id, :date, :type, :description, 
    :cost, :duration_hours, :status, :notes
);

-- Obter todos os registros de manutenção com filtros e paginação
SELECT m.*, p.name as project_name 
FROM landscaping_maintenance m
JOIN landscaping_projects p ON m.project_id = p.id
WHERE m.user_id = :user_id
    AND (:project_id IS NULL OR m.project_id = :project_id)
    AND (:type IS NULL OR m.type = :type)
    AND (:status IS NULL OR m.status = :status)
ORDER BY m.date DESC
LIMIT :limit OFFSET :offset;

-- Contar total de registros de manutenção com filtros
SELECT COUNT(*) FROM landscaping_maintenance 
WHERE user_id = :user_id
    AND (:project_id IS NULL OR project_id = :project_id)
    AND (:type IS NULL OR type = :type)
    AND (:status IS NULL OR status = :status);

-- Obter um registro de manutenção específico
SELECT m.*, p.name as project_name 
FROM landscaping_maintenance m
JOIN landscaping_projects p ON m.project_id = p.id
WHERE m.id = :maintenance_id;

-- Atualizar um registro de manutenção
UPDATE landscaping_maintenance
SET 
    project_id = COALESCE(:project_id, project_id),
    date = COALESCE(:date, date),
    type = COALESCE(:type, type),
    description = COALESCE(:description, description),
    cost = COALESCE(:cost, cost),
    duration_hours = COALESCE(:duration_hours, duration_hours),
    status = COALESCE(:status, status),
    notes = COALESCE(:notes, notes)
WHERE id = :maintenance_id AND user_id = :user_id;

-- Excluir um registro de manutenção
DELETE FROM landscaping_maintenance 
WHERE id = :maintenance_id AND user_id = :user_id;

-- Consultas adicionais

-- Obter resumo de custos de manutenção por projeto
SELECT 
    p.id as project_id,
    p.name as project_name,
    COUNT(m.id) as maintenance_count,
    SUM(m.cost) as total_cost,
    SUM(m.duration_hours) as total_hours
FROM landscaping_projects p
LEFT JOIN landscaping_maintenance m ON p.id = m.project_id
WHERE p.user_id = :user_id
GROUP BY p.id, p.name
ORDER BY p.name;