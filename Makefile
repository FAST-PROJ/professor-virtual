# Makefile for Docker Nginx PHP Composer MySQL

include .env

# MySQL
MYSQL_DUMPS_DIR=data/db/dumps

help:
	@echo ""
	@echo "Uso: make Commands"
	@echo ""
	@echo "Commands:"
	@echo "  start               Iniciar todos os serviços"
	@echo "  stop                Parar todos os serviços"

start:
	@docker-compose up -d

stop:
	@docker-compose down -v

logs:
	@docker-compose logs -f

mysql-create-all:
	@echo "Restaurando todas as bases de dados..."
	@mysql -h 127.0.0.1 -u"$(MYSQL_ROOT_USER)" -p"$(MYSQL_ROOT_PASSWORD)" <  .$(MYSQL_FILE_DIR)text.sql

install-dependencies:
	@echo "Instalando todas as dependencias do python"
	@pip install pdfminer.six
	@pip install PyMySQL
	@pip install SQLAlchemy
