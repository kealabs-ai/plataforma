-- Criação do banco de dados para n8n
CREATE DATABASE IF NOT EXISTS n8n_db;
GRANT ALL PRIVILEGES ON n8n_db.* TO 'root'@'%';
FLUSH PRIVILEGES;