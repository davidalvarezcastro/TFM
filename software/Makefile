# ****************************************************
# * Fichero con funciones directas sobre el proyecto *
# ****************************************************
include .env

# HELP
help:  ## Lista de comandos con su descripcion     
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


deploy: ## Despliega el sistema
	@docker-compose up
