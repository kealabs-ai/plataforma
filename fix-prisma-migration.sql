-- Script para corrigir migração falhada do Prisma
-- Baseado em: https://www.prisma.io/docs/orm/prisma-migrate/workflows/patching-and-hotfixing#failed-migration

-- 1. Marcar todas as migrações falhadas como aplicadas
UPDATE "_prisma_migrations" 
SET "finished_at" = NOW(), 
    "applied_steps_count" = 1,
    "logs" = 'Migration marked as resolved manually'
WHERE "finished_at" IS NULL;

-- Marcar migrações específicas conhecidas
UPDATE "_prisma_migrations" 
SET "finished_at" = NOW(), 
    "applied_steps_count" = 1,
    "logs" = 'Migration marked as resolved manually'
WHERE "migration_name" IN ('20240809105427_init', '20240609181238_init') 
  AND "finished_at" IS NULL;

-- 2. Se a tabela _prisma_migrations não existir, criar e inserir o registro
CREATE TABLE IF NOT EXISTS "_prisma_migrations" (
    "id" VARCHAR(36) NOT NULL,
    "checksum" VARCHAR(64) NOT NULL,
    "finished_at" TIMESTAMPTZ,
    "migration_name" VARCHAR(255) NOT NULL,
    "logs" TEXT,
    "rolled_back_at" TIMESTAMPTZ,
    "started_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "applied_steps_count" INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT "_prisma_migrations_pkey" PRIMARY KEY ("id")
);

-- 3. Inserir registro da migração como concluída
INSERT INTO "_prisma_migrations" (
    "id", 
    "checksum", 
    "migration_name", 
    "started_at", 
    "finished_at",
    "applied_steps_count",
    "logs"
) VALUES (
    '20240809105427_init',
    '0',
    '20240809105427_init',
    NOW(),
    NOW(),
    1,
    'Migration resolved manually - schema already applied'
) ON CONFLICT ("id") DO UPDATE SET
    "finished_at" = NOW(),
    "applied_steps_count" = 1,
    "logs" = 'Migration resolved manually - schema already applied';

-- 4. Verificar se todas as tabelas necessárias existem
DO $$
BEGIN
    -- Se as tabelas não existirem, o schema será aplicado automaticamente
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Instance') THEN
        RAISE NOTICE 'Tabelas não encontradas - schema será aplicado';
    ELSE
        RAISE NOTICE 'Schema já existe - migração marcada como concluída';
    END IF;
END $$;