from flask_sqlalchemy import SQLAlchemy
import boto3
import json
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
import logging

log = logging.getLogger(__name__)
db = SQLAlchemy()

def get_secret_manager_db():
    secret_name = "rds!cluster-9b4b7cd8-22ee-48ff-bbc4-d1f43ddf3bc8"
    region_name = "us-east-1"

    try:
        client = boto3.client("secretsmanager", region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        secret["host"] = secret.get("host", "cluster-gamer-vault.cluster-c6r6ws4k4vwo.us-east-1.rds.amazonaws.com:3306")
        secret["dbname"] = secret.get("dbname", "gamervaultlts")
        return secret
    except ClientError as e:
        log.error(f"Error al obtener el secreto: {e}")
        raise Exception("No se pudieron obtener las credenciales de la base de datos.") from e

def init_app(app):
    try:
        # Usamos una URI inicial vacía o falsa solo para inicializar SQLAlchemy
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://temp:temp@localhost/temp"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        # Reemplazamos el engine con uno dinámico
        def create_dynamic_engine():
            creds = get_secret_manager_db()
            uri = f"mysql+mysqlconnector://{creds['username']}:{creds['password']}@{creds['host']}/{creds['dbname']}"
            engine = create_engine(uri, pool_pre_ping=True)
            return engine

        with app.app_context():
            # Sustituimos el engine que usa SQLAlchemy
            db.engine = create_dynamic_engine()

            # Verificamos conexión
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                log.info("Conexión exitosa a la base de datos con secreto dinámico")
    except Exception as e:
        log.critical("Error crítico al configurar la base de datos: %s", str(e))
        raise Exception("Error crítico: No se pudo configurar la base de datos.") from e
