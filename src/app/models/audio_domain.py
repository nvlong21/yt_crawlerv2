from sqlalchemy import String, DateTime
from datetime import UTC, datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class AudioDomain(Base):
    __tablename__ = "AudioDomain"
    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    domain: Mapped[str] = mapped_column(String, nullable=True)
    describe: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)      