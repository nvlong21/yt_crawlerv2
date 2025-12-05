from datetime import UTC, datetime
import uuid as uuid_pkg
from sqlalchemy import String, Integer, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7
from ..core.db.database import Base


class AudioCraw(Base):
    __tablename__ = "AudioCraw"
    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    audio_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid7, unique=True)
    video_platform: Mapped[str] = mapped_column(String, nullable=True, default=None)
    platform_url: Mapped[str] = mapped_column(String, nullable=False, default= "")
    audio_url: Mapped[str] = mapped_column(String, nullable=True, default= "")
    duration: Mapped[int] = mapped_column(Integer, nullable=True, default= "")
    lang: Mapped[str] = mapped_column(String, nullable=True, default= "")
    subtitle: Mapped[str] = mapped_column(String, nullable=True, default= "")
    domain: Mapped[str] = mapped_column(String, nullable=True, default= "")
    caption_downloaded: Mapped[bool] = mapped_column(default=False)
    caption_url: Mapped[str] = mapped_column(String, nullable=True, default= "")    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)    
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)    