"""
Fichero para gestionar las diferentes acciones sobre el backend
"""

import click
import subprocess
import os
from sqlalchemy import event

import src.database.models # importamos los modelos para poder inicializar la base de datos

from src.settings import db_settings
from src.database.mysql import SQLALCHEMY_DATABASE_URL, Base, engine
from src.database.data_mysql import initialize_table_crops, initialize_table_model_type


SQL_CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {database}"
SQL_GRANT_DATABASE = "GRANT ALL PRIVILEGES ON {database}.* TO {user}@\"%\""


@click.group()
def cli():
    pass

@cli.command(help='ejecuta el script para descargar las imágenes utilizadas para las CNN')
def getimageslayers():
    # se ejecutan los scripts externos
    python_tests_cmd = [
        'python',
        'src/data/get_images_CNN.py'
    ]
    python_tests_cmd.extend({})
    subprocess.call(' '.join(python_tests_cmd), shell=True)

@cli.command(help='Inicia la base de datos (CUIDADO)')
def dbinit():
    # setting up eventos bafore table creation (populates tables)
    event.listen(src.database.models.CropValueORM.__table__, 'after_create', initialize_table_crops)
    event.listen(src.database.models.ModelTypeORM.__table__, 'after_create', initialize_table_model_type)
    
    base = "mysql \
        --user='{user}' --port={port} \
        --host='{host}' --password='{password}' ".format(
        user='root',
        port=db_settings.PORT,
        host=db_settings.HOST,
        password=db_settings.ROOT_PASSWORD
    )

    # creamos la base de datos
    sql_crear = base + " -e '{sql}'".format(
        sql=SQL_CREATE_DATABASE.format(database=db_settings.DATABASE)
    )
    os.system(sql_crear)

    # privilegios sobre la base de datos
    sql_grant = base + " -e '{sql}'".format(
        sql=SQL_GRANT_DATABASE.format(
            user=db_settings.USER,
            database=db_settings.DATABASE
        )
    )
    os.system(sql_grant)

    # creamos las tablas en la base de datos
    Base.metadata.create_all(bind=engine)


@cli.command(help='actualiza los modelos de la aplicación a partir de las tablas definidas en la base de datos relacional')
def dbmodels():
    python_tests_cmd = [
        'sqlacodegen',
        SQLALCHEMY_DATABASE_URL,
        '>',
        'src/database/models_no_git.py'
    ]
    python_tests_cmd.extend({})
    subprocess.call(' '.join(python_tests_cmd), shell=True)


# @cli.command(help='inicia el servicio de gestión de colisiones')
# def servicio_gestion_flota():
#     ServicioControlFlota.run(
#         logs=settings.SERVICE_CONTROL_FLOTA_LOGS,
#         tests=settings.SERVICE_CONTROL_FLOTA_TESTS,
#         rosbridge=settings.SERVICE_CONTROL_FLOTA_ROSBRIDGE,
#         sniffer=settings.SERVICE_CONTROL_FLOTA_SNIFFER)


# @cli.command(help='inicia la base de datos relacional')
# def db_init():
#     base = "mysql \
#         --user='{user}' --port={port} \
#         --host='{host}' --password='{password}' ".format(
#         user=settings.DB_ROOT_USER,
#         port=settings.DB_PORT,
#         host=settings.DB_HOST,
#         password=settings.DB_ROOT_PASSWORD
#     )

#     # creamos la base de datos
#     sql_crear = base + " -e '{sql}'".format(
#         sql=SQL_CREATE_DATABASE.format(database=settings.DB_DATABASE)
#     )
#     os.system(sql_crear)

#     # privilegios sobre la base de datos
#     sql_grant = base + " -e '{sql}'".format(
#         sql=SQL_GRANT_DATABASE.format(
#             user=settings.DB_USER,
#             database=settings.DB_DATABASE
#         )
#     )
#     os.system(sql_grant)
#     FactoriaApp.db().create_all()


# @cli.command(help='ejecuta las migraciones de la base de datos relacional')
# @click.option('-m', is_flag=True, help='crea una migración')
# @click.option('-u', is_flag=True, help='ejecuta las migraciones')
# @click.option('-d', is_flag=True, help='ejecuta tests de aceptación')
# @click.option('--message', help="mensaje informativo para la migración (-m)")
# def db_migration(m, u, d, message=None):
#     with FactoriaApp.app().app_context():
#         if m:
#             migrate(message=message)
#         if u:
#             upgrade()
#         if d:
#             downgrade()

# @cli.command(help='despliega el sistema en un contenedor iniciando todos los servicios especificados')
# def deploy():
#     # se comprueba que contenedores son necesarios desplegar
#     servicios_externos = [
#         {'name': 'CF_MQTT_DOCKER', 'container': DOCKER_SGE_NAME},
#         {'name': 'CF_DB_DOCKER', 'container': DOCKER_DB_SQL_NAME},
#         {'name': 'CF_MONGODB_DOCKER', 'container': DOCKER_DB_NOSQL_NAME},
#     ]

#     lista_contenedores = " ".join(
#         [x['container'] for x in servicios_externos if bool(int(os.getenv(x['name'])))] + [DOCKER_COLISIONES_NAME, DOCKER_API_NAME])

#     up_container(lista_contenedores, build=True)


# @cli.command(help='ejecuta test definidos')
# @click.option('--unit', is_flag=True, help='ejecuta tests unitarios')
# @click.option('--integration', is_flag=True, help='ejecuta tests de integración')
# @click.option('--acceptance', is_flag=True, help='ejecuta tests de aceptación')
# @click.option('--all', is_flag=True, help='ejecuta todos los test definidos')
# @click.option('--coverage', is_flag=True, help='calcula el coverage')
# @click.option('--browser', is_flag=True, help='abre el informe de coverage en un navegador')
# @click.option('--scripts', is_flag=True, help='ejecuta los tests definidos por medio de scripts')
# @click.argument('args', nargs=-1)
# def test(unit, integration, acceptance, all, coverage, browser, scripts, args):
#     os.environ['MODE'] = settings.MODE_TEST

#     # puertos para el servicio de testing
#     if not scripts:
#         os.environ['CF_SGE_PORT_BINDED'] = "1889"
#         os.environ['CF_SGE_WEB_PORT_BINDED'] = "8889"

#     if unit or all:
#         os.environ['UNIT_TESTS'] = '1'
#     if integration or all:
#         os.environ['INTEGRATION_TESTS'] = '1'
#         # creación de la base de datos
#     if acceptance or all:
#         os.environ['ACCEPTANCE_TESTS'] = '1'
#         # hacer lo que haya que hacer

#     if coverage:
#         python_tests_cmd = [
#             'coverage',
#             'run',
#             '--omit',
#             '\'venv/*, test/*\'',
#             '-m',
#             'unittest',
#             'tests/__main__.py',
#             # 'tests/unit/api/test_api_historico_mock_dao.py',
#             '&&',
#             'coverage',
#             'html',
#             '-d',
#             'coverage',
#             '&&',
#             'coverage',
#             'report',
#         ]

#         if browser:
#             python_tests_cmd = python_tests_cmd + [
#                 '&&',
#                 'browse',
#                 'coverage/index.html',
#             ]

#     else:
#         python_tests_cmd = [
#             'python',
#             '-m',
#             'unittest',
#             'tests/__main__.py'
#         ]

#     python_tests_cmd.extend(args)

#     if unit or integration or acceptance or all:
#         # levantamos los contenedores
#         up_container(DOCKER_SGE_TESTING_NAME, file=DOCKER_COMPOSE_TESTING_FILE)
#         subprocess.call(' '.join(python_tests_cmd), shell=True)
#         # apagamos los contenedores
#         down_container(DOCKER_SGE_TESTING_NAME)

#     if scripts:
#         # se ejecutan los scripts externos
#         python_tests_cmd = [
#             'python',
#             'tests/scripts/__main__.py'
#             # 'tests/scripts/deploy_cf.py'
#         ]
#         python_tests_cmd.extend(args)
#         subprocess.call(' '.join(python_tests_cmd), shell=True)


if __name__ == '__main__':
    cli()

