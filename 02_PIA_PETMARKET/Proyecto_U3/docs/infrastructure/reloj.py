"""Abstracción de reloj para pruebas y registros con UTC."""
from datetime import datetime,timezone
class RelojSistema:
    def ahora(self)->datetime:return datetime.now(timezone.utc)
class RelojFijo:
    def __init__(self,instante:datetime):self.instante=instante
    def ahora(self)->datetime:return self.instante
