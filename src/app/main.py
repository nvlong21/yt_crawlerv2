from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from .core.setup import create_tables
from .core.config import settings
from .crawler import create_application
import asyncio
create_tables()
app = create_application()
# video_ids = app.youtube_search("politics", 1)
video_ids = app.bilibili_search("politics", 1)
# uniqueIds = app.filter_duplicate(video_ids)
# print(uniqueIds)
# app.download_audio(["https://www.youtube.com/watch?v=Mn6GHMA8GIs"])
# app.download_captions()