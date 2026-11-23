"""Agenda, presupuesto y paletas; continuación del merge de tareas y tema."""
from alembic import op
import sqlalchemy as sa
revision = "e62b903a47f1"
down_revision = "7d297b6ad7b3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("actividades_agenda",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("evento_id", sa.Integer(), sa.ForeignKey("eventos.id"), nullable=False),
        sa.Column("titulo", sa.String(150), nullable=False),
        sa.Column("descripcion", sa.Text()), sa.Column("responsable", sa.String(150)),
        sa.Column("inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fin", sa.DateTime(timezone=True), nullable=False),
        sa.Column("creado_en", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("fin > inicio", name="ck_agenda_orden_fechas"))
    op.create_index("ix_actividades_agenda_evento_id", "actividades_agenda", ["evento_id"])
    op.create_table("presupuestos",
        sa.Column("evento_id", sa.Integer(), sa.ForeignKey("eventos.id"), primary_key=True),
        sa.Column("limite", sa.Numeric(12, 2), nullable=False),
        sa.CheckConstraint("limite >= 0", name="ck_presupuesto_limite"))
    op.create_table("gastos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("evento_id", sa.Integer(), sa.ForeignKey("eventos.id"), nullable=False),
        sa.Column("concepto", sa.String(150), nullable=False),
        sa.Column("categoria", sa.String(80), nullable=False), sa.Column("notas", sa.Text()),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("pagado", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("creado_en", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("valor > 0", name="ck_gasto_valor"))
    op.create_index("ix_gastos_evento_id", "gastos", ["evento_id"])
    op.execute("UPDATE usuarios SET tema = CASE WHEN tema = 'rosa' THEN 'vino' ELSE 'azul' END WHERE tema NOT IN ('azul', 'verde', 'vino', 'terracota')")
    with op.batch_alter_table("usuarios") as batch:
        batch.alter_column("tema", existing_type=sa.String(16), nullable=False, server_default="azul")


def downgrade():
    op.execute("UPDATE usuarios SET tema = 'rosa' WHERE tema = 'vino'")
    op.execute("UPDATE usuarios SET tema = 'violeta' WHERE tema = 'terracota'")
    with op.batch_alter_table("usuarios") as batch:
        batch.alter_column("tema", existing_type=sa.String(16), nullable=False, server_default="violeta")
    op.drop_index("ix_gastos_evento_id", table_name="gastos")
    op.drop_table("gastos")
    op.drop_table("presupuestos")
    op.drop_index("ix_actividades_agenda_evento_id", table_name="actividades_agenda")
    op.drop_table("actividades_agenda")
