"""UoW en memoria con restauración de instantáneas de repositorios enlazados.
No proporciona durabilidad, bloqueos ni transacciones ACID de base de datos.
"""
from copy import deepcopy
class UnidadTrabajoSnapshot:
    def __init__(self,*repositorios):
        self.repositorios=repositorios
        self.eventos=[]
        self._instantaneas=None
    def iniciar(self):
        if self._instantaneas is not None:raise RuntimeError('Transacción local activa')
        self._instantaneas=[deepcopy(repo.datos) for repo in self.repositorios]
        self.eventos.append('iniciar')
    def confirmar(self):
        if self._instantaneas is None:raise RuntimeError('No hay transacción activa')
        self._instantaneas=None
        self.eventos.append('confirmar')
    def revertir(self):
        if self._instantaneas is None:raise RuntimeError('No hay transacción activa')
        for repo,datos in zip(self.repositorios,self._instantaneas):repo.datos=datos
        self._instantaneas=None
        self.eventos.append('revertir')
