from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema

class AudioCrawBase(BaseModel):
    audio_id: Annotated[str, Field(min_length=2, max_length=100, examples=["hYU4b-UnCQA&list=RDhYU4b-UnCQA"])]

class AudioCrawCreate(TimestampSchema, AudioCrawBase, UUIDSchema, PersistentDeletion):
    video_platform: str
    platform_url: str
    audio_url: str
    duration: int
    lang: str
    subtitle: str
    domain: str


class AudioCrawRead(BaseModel):
    id: int
    audio_id: Annotated[str, Field(min_length=2, max_length=100, examples=["hYU4b-UnCQA&list=RDhYU4b-UnCQA"])]
    video_platform: Annotated[str, Field(min_length=2, max_length=30, examples=["youtube"])]
    lang: Annotated[str, Field(min_length=1, max_length=20, examples=["vn"])]
    domain: Annotated[str, Field(min_length=1, max_length=20, examples=[""])]
    created_at: datetime

class AudioCrawUpdate(BaseModel):
    video_platform: str
    platform_url: str
    audio_url: str
    duration: int
    lang: str
    subtitle: str
    domain: str
    caption_downloaded: bool
    caption_url: str

class AudioCrawUpdateInternal(AudioCrawUpdate):
    updated_at: datetime


class AudioCrawDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_deleted: bool
    deleted_at: datetime
