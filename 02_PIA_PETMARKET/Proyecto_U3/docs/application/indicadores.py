"""Consulta agregada para el responsable del negocio; no altera agregados."""
from datetime import datetime
from domain.metricas import calcular_indicadores
class IndicadoresApplicationService:
    def __init__(self,pedidos):self.pedidos=pedidos
    def consultar(self,desde:datetime|None=None,hasta:datetime|None=None)->dict:
        if desde and hasta and desde>hasta:raise ValueError('Rango de fechas inválido')
        return calcular_indicadores(self.pedidos.listar(),desde,hasta)
