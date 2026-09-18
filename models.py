from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class OwnerEnum(str, Enum):
    """
    Enumeración para el propietario de la transacción o el estado de revisión.
    """
    PERSONAL = "Personal"
    COMPARTIDO = "Compartido"
    REVISAR = "Revisar"
    REVISION = "Revisión"
    CONFIRMAR = "Confirmar"

class RawTransaction(BaseModel):
    """
    Modelo para la transacción original (cruda) extraída de la cartola bancaria.
    """
    date_str: str = Field(..., description="Fecha original de la cartola")
    description: str = Field(..., description="Glosa original de la transacción")
    amount: float = Field(..., description="Monto crudo de la transacción")
    currency: str = Field(default="CLP", description="Moneda de la transacción, por defecto 'CLP'")
    is_credit: bool = Field(default=False, description="True para abonos, sueldos, devoluciones o pagos de tarjeta")
    source: str = Field(..., description="Fuente o producto (ej. 'Cuenta Corriente', 'TC Nacional', 'TC Internacional')")

class ProcessedTransaction(BaseModel):
    """
    Modelo para la transacción procesada y categorizada, lista para ser insertada en Google Sheets.
    """
    fecha: str = Field(..., description="Fecha en formato procesado")
    descripcion: str = Field(..., description="Descripción limpia o estandarizada")
    monto: int = Field(..., description="Monto 'Clean Sheets': estrictamente entero sin decimales ni formato")
    categoria: str = Field(..., description="Categoría del gasto o ingreso")
    owner: str = Field(..., description="Propietario (usualmente un valor de OwnerEnum)")
    notas: str = Field(default="", description="Notas adicionales (ej. detalle propuesto por IA)")

    def to_pipe_row(self) -> str:
        """
        Retorna la fila con formato separado por pipe exacto:
        'Fecha | Descripción | Monto | Categoría | Owner | Notas'
        """
        return f"{self.fecha} | {self.descripcion} | {self.monto} | {self.categoria} | {self.owner} | {self.notas}"

class ReconciliationReport(BaseModel):
    """
    Modelo que representa el reporte final de la conciliación bancaria tras procesar las transacciones.
    """
    transactions: List[ProcessedTransaction] = Field(..., description="Lista de transacciones procesadas")
    total_cargos_calculado: int = Field(..., description="Suma de los montos de cargos procesados")
    total_cargos_esperado: Optional[int] = Field(default=None, description="Suma de cargos esperados según resumen bancario")
    diferencia: int = Field(..., description="Diferencia entre lo calculado y lo esperado")
    cuadratura_ok: bool = Field(..., description="True si la conciliación cuadra (diferencia == 0)")
    unmapped_count: int = Field(..., description="Cantidad de transacciones que requirieron propuesta IA")
