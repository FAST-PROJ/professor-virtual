# Makefile for Docker Nginx PHP Composer MySQL

include .env

# MySQL
MYSQL_DUMPS_DIR=data/db/dumps

help:
	@echo ""
	@echo "Uso: make Commands"
	@echo ""
	@echo "Commands:"
	@echo "  start-with-db        Iniciar todos os serviços com o dump da base de dados"
	@echo "  start                Iniciar todos os serviços"
	@echo "  stop                 Parar todos os serviços"
	@echo "  install-dependencies Instalar todas as dependências do projeto"
	@echo "  fixphp               Ajustar as permissões das pastas do app"
	@echo "  resetOwner           Ajustar as permissões para o usuário root"
	@echo "  mysql-restore-db    Restaurar o backup e um banco de dados especifico (mysql-restore-db DATABASE='DATABASE_NAME')"
	@echo "  mysql-dump-db       Criar backup de um banco de dados especifico (mysql-dump-db DATABASE='DATABASE_NAME')"

start:
	@docker-compose up -d

stop:
	@docker-compose down -v

logs:
	@docker-compose logs -f

mysql-create-all:
	@echo "Restaurando todas as bases de dados..."
	@mysql -h 127.0.0.1 -u"$(MYSQL_ROOT_USER)" -p"$(MYSQL_ROOT_PASSWORD)" <  .$(MYSQL_FILE_DIR)text.sql

fixphp:
	@echo "Ajustando as permissões das pastas..."
	@$(shell chown -Rf 1000:www-data "$(shell pwd)/web/app/storage" 2> /dev/null)
	@$(shell chmod -R 755 "$(shell pwd)/web/app/storage" 2> /dev/null)

resetOwner:
	@$(shell chown -Rf $(SUDO_USER):$(shell id -g -n $(SUDO_USER)) $(MYSQL_DUMPS_DIR) "$(shell pwd)/etc/ssl" "$(shell pwd)/web/app" 2> /dev/null)

start-with-db: start
	@echo "Iniciando o projeto com a base de dados do desafio de busca..."
	@make mysql-restore-db DATABASE='selene'

mysql-restore-db:
	@echo "Restaurando a base de dados $$DATABASE..."
	@docker exec -i $(shell docker-compose ps -q mysqldb) mysql -u"$(MYSQL_ROOT_USER)" -p"$(MYSQL_ROOT_PASSWORD)" < $(MYSQL_DUMPS_DIR)/$$DATABASE.sql 2>/dev/null

mysql-dump-db:
	@echo "Fazendo backup da base de dados $$DATABASE..."
	@mkdir -p $(MYSQL_DUMPS_DIR)
	@docker exec $(shell docker-compose ps -q mysqldb) mysqldump --all-databases -u"$(MYSQL_ROOT_USER)" -p"$(MYSQL_ROOT_PASSWORD)" > $(MYSQL_DUMPS_DIR)/$$DATABASE.sql 2>/dev/null
	@make resetOwner

install-dependencies:
	@echo "Instalando todas as dependencias do python"
	@pip install pdfminer.six
	@pip install PyMySQL
	@pip install SQLAlchemy
	@pip install Flask
