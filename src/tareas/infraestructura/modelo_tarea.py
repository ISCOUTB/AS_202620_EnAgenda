from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.usuarios.infraestructura.modelo_usuario import Base


class TareaModelo(Base):
    __tablename__ = "tareas"
    __table_args__ = (
        CheckConstraint(
            "length(trim(titulo)) > 0",
            name="ck_tareas_titulo_no_vacio",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    evento_id: Mapped[int] = mapped_column(
        ForeignKey("eventos.id"),
        nullable=False,
        index=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    completada: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("CURRENT_TIMESTAMP"),
    )