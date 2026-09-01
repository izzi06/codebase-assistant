from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class RepositoryFile(Base):
    __tablename__ = "repository_files"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "path",
            name="uq_repository_files_project_path",
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("projects.id", ondelete="Cascade"),
        nullable=False,
        index=True,
    )
    path: Mapped[String] = mapped_column(
        String(1000),
        nullable=False,
    )
    extension: Mapped[String] = mapped_column(
        String(50),
        nullable=False,
    )
    size_bytes: Mapped[BigInteger] = mapped_column(
        BigInteger,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
