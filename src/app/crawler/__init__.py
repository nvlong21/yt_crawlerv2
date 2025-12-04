from typing import Any
from .crawler import AudioCrawler 
# -------------- application --------------
def create_application(
    **kwargs: Any,
) -> AudioCrawler:
    application = AudioCrawler(**kwargs)
    return application