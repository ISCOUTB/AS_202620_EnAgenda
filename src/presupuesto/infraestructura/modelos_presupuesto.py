from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column
from src.usuarios.infraestructura.modelo_usuario import Base


class PresupuestoModelo(Base):
    __tablename__ = "presupuestos"
    __table_args__ = (CheckConstraint("limite >= 0", name="ck_presupuesto_limite"),)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id"), primary_key=True)
    limite: Mapped[Decimal] = mapped_column(Numeric(12, 2))


class GastoModelo(Base):
    __tablename__ = "gastos"
    __table_args__ = (CheckConstraint("valor > 0", name="ck_gasto_valor"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id"), index=True)
    concepto: Mapped[str] = mapped_column(String(150))
    categoria: Mapped[str] = mapped_column(String(80))
    notas: Mapped[str | None] = mapped_column(Text)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    pagado: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
