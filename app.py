import os
import sys
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from models.database.databasemodel import db as db

from models.api.endpoint import ApiEndpoint
from models.routes.dashboard import Dashboard

def load_env():
    if os.path.exists('.env'):
        print('Importing environment from .env...')
        load_dotenv()

        dbusername = os.getenv('POSTGRES_ENV_USER')
        dbpassword = os.getenv('POSTGRES_ENV_PASSWORD')
        dbname = os.getenv('POSTGRES_ENV_DATABASE')
        dbhost = "localhost"  # cause it would mean we are outside the docker container and we need to connect to the docker container
        dbport = os.getenv('POSTGRES_ENV_PORT')

    else:
        dbusername = os.getenv('POSTGRES_ENV_USER') if os.getenv('POSTGRES_ENV_USER') else ""
        dbpassword = os.getenv('POSTGRES_ENV_PASSWORD') if os.getenv('POSTGRES_ENV_PASSWORD') else ""
        dbname = os.getenv('POSTGRES_ENV_DATABASE') if os.getenv('POSTGRES_ENV_DATABASE') else ""
        dbhost = os.getenv('POSTGRES_ENV_HOSTNAME') if os.getenv('POSTGRES_ENV_HOSTNAME') else "postgredb"
        dbport = os.getenv('POSTGRES_ENV_PORT') if os.getenv('POSTGRES_ENV_PORT') else "5432"

    return dbusername, dbpassword, dbname, dbhost, dbport


def create_app():
    dbusername, dbpassword, dbname, dbhost, dbport = load_env()

    app = Flask(__name__, static_url_path='/static')
    api = Api(app)

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'postgresql://' + dbusername + ':' + dbpassword + '@' + dbhost + ':' + dbport + '/' + dbname,
        'MAX_CONTENT_LENGTH': 32 * 1024 * 1024,
        'PERMANENT_SESSION_LIFETIME': timedelta(days=30),
    })

    api.add_resource(ApiEndpoint, '/api/endpoint')
    api.add_resource(Dashboard, '/')

    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)


if __name__ == '__main__':
    ARGDEBUG = len(sys.argv) > 1 and sys.argv[1] in ('-d', '--debug')
    app = create_app()
    app.run(debug=ARGDEBUG, host='0.0.0.0')



