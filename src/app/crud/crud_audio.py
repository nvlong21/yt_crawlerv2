from fastcrud import FastCRUD

from ..models.audio_craw import AudioCraw
from ..schemas.audio_craw import *

CRUDAudio = FastCRUD[AudioCraw, AudioCrawCreate, AudioCrawUpdate, AudioCrawRead, AudioCrawUpdateInternal, AudioCrawDelete]
crud_audios = CRUDAudio(AudioCraw)
