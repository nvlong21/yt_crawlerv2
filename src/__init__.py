from .app.core.setup import create_tables
from .app.crawler import create_application
if __name__ == "__main__":
    create_tables()
    app = create_application()
    videoEntries = app.youtube_search("politics", 2)
    print(videoEntries)
    # video_ids = app.bilibili_search("politics", 1)
    uniqueIds = app.filter_duplicate(videoEntries)
    # print(uniqueIds)
    app.download_and_upload_audio(uniqueIds)
    # app.download_captions()