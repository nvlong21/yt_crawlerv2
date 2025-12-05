from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from .core.setup import create_tables
from .crawler import create_application
import asyncio
create_tables()
app = create_application()
videoEntries = app.youtube_search("politics", 2)
# video_ids = app.bilibili_search("politics", 1)
uniqueIds = app.filter_duplicate(videoEntries)
# print(uniqueIds)
app.download_and_upload_audio(uniqueIds)
# app.download_captions()