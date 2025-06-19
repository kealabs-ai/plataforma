-- Criar banco de dados para o n8n se não existir
CREATE DATABASE IF NOT EXISTS n8n_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Garantir que o usuário root tenha acesso ao banco de dados n8n_db
GRANT ALL PRIVILEGES ON n8n_db.* TO 'root'@'%';
FLUSH PRIVILEGES;