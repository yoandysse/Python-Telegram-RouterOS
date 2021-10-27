import db
from sqlalchemy import Column, Integer, String


class GestionUsuarios(db.Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    idTelegram = Column(Integer)
    usernameTelegram = Column(String, nullable=False)
    cuenta = Column(String, unique=True)


    def __init__(self, idTelegram, usernameTelegram):
        self.idTelegram = idTelegram
        self.usernameTelegram = usernameTelegram
        self.cuenta = None

    def __str__(self):
        return "Usuario de Telegram: {} asignado a Cuenta:{}".format(self.usernameTelegram, self.cuenta)
