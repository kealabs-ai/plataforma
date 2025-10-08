# Deploy Guide - Kealabs Intelligence

## 🚀 Deploy na VPS Hostinger

### Pré-requisitos
- VPS com Ubuntu/Debian
- Docker instalado
- Git instalado
- Portas 8000 e 8501 liberadas

### 1. Configuração Inicial

```bash
# Clonar repositório
git clone https://github.com/kealabs-ai/plataforma.git
cd plataforma

# Dar permissões aos scripts
chmod +x deploy.sh
chmod +x docker-healthcheck.sh
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de produção
cp .env.production .env

# Editar configurações específicas
nano .env
```

### 3. Deploy Manual

```bash
# Executar script de deploy
./deploy.sh
```

### 4. Verificar Deploy

```bash
# Verificar saúde dos serviços
./docker-healthcheck.sh

# Verificar logs
docker logs kealabs-api
docker logs kealabs-frontend
```

## 🔄 Deploy via Jenkins

### Configuração do Jenkins

1. **Criar Pipeline Job**
   - New Item → Pipeline
   - Nome: `kealabs-intelligence-deploy`

2. **Configurar SCM**
   - Repository URL: `https://github.com/kealabs-ai/plataforma.git`
   - Credentials: Configurar token GitHub
   - Branch: `*/main` ou `*/develop`

3. **Pipeline Script**
   - Definition: Pipeline script from SCM
   - Script Path: `Jenkinsfile`

### Branches e Ambientes

- **develop**: Deploy automático em ambiente de desenvolvimento
- **main**: Deploy automático em ambiente de produção

## 📊 Monitoramento

### URLs de Acesso
- **API**: http://seu-ip:8000
- **Frontend**: http://seu-ip:8501
- **Health Check API**: http://seu-ip:8000/status

### Comandos Úteis

```bash
# Ver containers rodando
docker ps --filter "name=kealabs-"

# Ver logs em tempo real
docker logs -f kealabs-api
docker logs -f kealabs-frontend

# Reiniciar serviços
docker restart kealabs-api kealabs-frontend

# Parar todos os serviços
docker stop kealabs-api kealabs-frontend
docker rm kealabs-api kealabs-frontend
```

## 🔧 Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco**
   - Verificar configurações em `.env`
   - Testar conectividade: `telnet 72.60.140.128 2621`

2. **Container não inicia**
   - Verificar logs: `docker logs kealabs-api`
   - Verificar recursos: `docker stats`

3. **Porta já em uso**
   - Verificar processos: `netstat -tulpn | grep :8000`
   - Parar processo: `sudo kill -9 PID`

### Logs Importantes

```bash
# Logs do sistema
journalctl -u docker

# Logs da aplicação
docker logs kealabs-api --since 1h
docker logs kealabs-frontend --since 1h
```

## 🔒 Segurança

### Configurações Recomendadas

1. **Firewall**
   ```bash
   sudo ufw allow 22
   sudo ufw allow 8000
   sudo ufw allow 8501
   sudo ufw enable
   ```

2. **SSL/TLS** (Opcional)
   - Configurar Nginx como proxy reverso
   - Usar Let's Encrypt para certificados

3. **Backup**
   - Backup regular do banco de dados
   - Backup dos arquivos de configuração

## 📈 Performance

### Otimizações

1. **Recursos Docker**
   ```bash
   # Limitar recursos se necessário
   docker update --memory=1g --cpus=1 kealabs-api
   ```

2. **Monitoramento**
   ```bash
   # Instalar htop para monitoramento
   sudo apt install htop
   ```

## 🆘 Suporte

Em caso de problemas:
1. Verificar logs dos containers
2. Executar health check
3. Verificar conectividade de rede
4. Contatar equipe de desenvolvimento