-- Queries para o módulo de Floricultura
-- Consultas SQL para operações CRUD nas tabelas de floricultura

-- OPERAÇÕES PARA CULTIVOS DE FLORES

-- Criar um novo cultivo de flores
INSERT INTO flower_cultivations (
    user_id, species, variety, planting_date, area_m2, 
    greenhouse_id, expected_harvest_date, status, notes
) VALUES (
    :user_id, :species, :variety, :planting_date, :area_m2, 
    :greenhouse_id, :expected_harvest_date, :status, :notes
);

-- Obter todos os cultivos de flores com filtros e paginação
SELECT * FROM flower_cultivations 
WHERE user_id = :user_id
    AND (:species IS NULL OR species = :species)
    AND (:status IS NULL OR status = :status)
    AND (:greenhouse_id IS NULL OR greenhouse_id = :greenhouse_id)
ORDER BY planting_date DESC
LIMIT :limit OFFSET :offset;

-- Contar total de cultivos de flores com filtros
SELECT COUNT(*) FROM flower_cultivations 
WHERE user_id = :user_id
    AND (:species IS NULL OR species = :species)
    AND (:status IS NULL OR status = :status)
    AND (:greenhouse_id IS NULL OR greenhouse_id = :greenhouse_id);

-- Obter um cultivo de flores específico
SELECT * FROM flower_cultivations 
WHERE id = :flower_id;

-- Atualizar um cultivo de flores
UPDATE flower_cultivations
SET 
    species = COALESCE(:species, species),
    variety = COALESCE(:variety, variety),
    planting_date = COALESCE(:planting_date, planting_date),
    area_m2 = COALESCE(:area_m2, area_m2),
    greenhouse_id = COALESCE(:greenhouse_id, greenhouse_id),
    expected_harvest_date = COALESCE(:expected_harvest_date, expected_harvest_date),
    status = COALESCE(:status, status),
    notes = COALESCE(:notes, notes)
WHERE id = :flower_id AND user_id = :user_id;

-- Excluir um cultivo de flores
DELETE FROM flower_cultivations 
WHERE id = :flower_id AND user_id = :user_id;

-- OPERAÇÕES PARA ESTUFAS

-- Criar uma nova estufa
INSERT INTO greenhouses (
    user_id, name, area_m2, type, temperature_control, 
    humidity_control, irrigation_system, location, notes
) VALUES (
    :user_id, :name, :area_m2, :type, :temperature_control, 
    :humidity_control, :irrigation_system, :location, :notes
);

-- Obter todas as estufas com filtros e paginação
SELECT * FROM greenhouses 
WHERE user_id = :user_id
    AND (:type IS NULL OR type = :type)
ORDER BY name
LIMIT :limit OFFSET :offset;

-- Contar total de estufas com filtros
SELECT COUNT(*) FROM greenhouses 
WHERE user_id = :user_id
    AND (:type IS NULL OR type = :type);

-- Obter uma estufa específica
SELECT * FROM greenhouses 
WHERE id = :greenhouse_id;

-- Atualizar uma estufa
UPDATE greenhouses
SET 
    name = COALESCE(:name, name),
    area_m2 = COALESCE(:area_m2, area_m2),
    type = COALESCE(:type, type),
    temperature_control = COALESCE(:temperature_control, temperature_control),
    humidity_control = COALESCE(:humidity_control, humidity_control),
    irrigation_system = COALESCE(:irrigation_system, irrigation_system),
    location = COALESCE(:location, location),
    notes = COALESCE(:notes, notes)
WHERE id = :greenhouse_id AND user_id = :user_id;

-- Excluir uma estufa
DELETE FROM greenhouses 
WHERE id = :greenhouse_id AND user_id = :user_id;

-- Consulta para obter estufas com contagem de cultivos
SELECT g.*, COUNT(f.id) as flower_count
FROM greenhouses g
LEFT JOIN flower_cultivations f ON g.id = f.greenhouse_id
WHERE g.user_id = :user_id
GROUP BY g.id
ORDER BY g.name
LIMIT :limit OFFSET :offset;