# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# El engine permite a sqlarchemy comunicarse con la bd
# https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine("sqlite:///database/users.db", connect_args={"check_same_thread": False})

# Crear la sesión es lo que permira operar dentro de la bd
Session = sessionmaker(bind=engine)
session = Session()

# se encarga de mapiar la clase en la bd
Base = declarative_base()

