import logging

import json
import os
import shutil
from sqlalchemy import select
from functools import partial
from glob import glob
import tqdm
import yt_dlp as youtube_dl
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi, Transcript
from youtube_transcript_api._errors import NoTranscriptFound
from ..core.config import settings
from ..core.db.database import get_db
from ..models.audio_craw import AudioCraw

import json


def split_with_caption(audio_path, skip_idx=0, out_ext="wav") -> list:
    df = pd.read_csv(audio_path.split('wavs')[0] + 'text/subtitle.csv')
    filename = os.path.basename(audio_path).split('.', 1)[0]

    audio = read_audio(audio_path)
    df2 = df[df['id'].apply(str) == filename]
    df2['end'] = round((df2['start'] + df2['duration']) * 1000).astype(int)
    df2['start'] = round(df2['start'] * 1000).astype(int)
    edges = df2[['start', 'end']].values.tolist()

    audio_paths = []
    for idx, (start_idx, end_idx) in enumerate(edges[skip_idx:]):
        start_idx = max(0, start_idx)

        target_audio_path = "{}/{}.{:04d}.{}".format(
            os.path.dirname(audio_path), filename, idx, out_ext)

        segment = audio[start_idx:end_idx]

        segment.export(target_audio_path, "wav")  # for soundsegment

        audio_paths.append(target_audio_path)

    return audio_paths


def read_audio(audio_path):
    return AudioSegment.from_file(audio_path)

class AudioCrawler:
    def __init__(self):
        # Delete directory if existing
        if os.path.exists(settings.DATA_DIR):
            shutil.rmtree(settings.DATA_DIR, ignore_errors=True)
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        self.lang = "en"

    def youtube_search(self, query, max_results=20):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,  # chỉ lấy metadata, không load streams
        }

        query_str = f"ytsearch{max_results}:{query}"

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query_str, download=False)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)              
        videos = result.get('entries', [])
        videoIds = [v['id'] for v in videos if 'id' in v]
        return videoIds

    def filter_duplicate(self, _videos: list[dict]):
        db = next(get_db())
        _vidIds = [v['id'] for v in _videos]
        try:
            _existingRows = db.query(AudioCraw.audio_id).filter(AudioCraw.audio_id.in_(_vidIds)).all()
            _existingIds = {row[0] for row in _existingRows}
            _uniqueVideos = [v for v in _videos if v['id'] not in _existingIds]
            return _uniqueVideos
        finally:
            db.close()
    def bilibili_search(keyword, max_results=5, out_dir="audio"):
        ydl_opts = {
            "format": "ba/best",
            "quiet": False,
            # "default_search": "bilisearch",  # yt-dlp builtin search Bilibili
            "skip_download": True, 
            # 'extract_flat': True,  # chỉ lấy metadata, không load streams
        }
        query_str = f"bilisearch1:{keyword}"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # yt-dlp sẽ search và download audio
            result = ydl.extract_info(query_str, download=False)
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)                
        # print(result)
    # Example
    # urls = youtube_search("japanese politics speech", 10)

    def download_audio(self, urls) -> None:
        download_path = os.path.join(settings.DATA_DIR, "wavs/" + '%(id)s.%(ext)s')
        # youtube_dl options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192'
            }],
            'postprocessors_args': [
                '-ar', '21000'
            ],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'outtmpl': download_path,  # 다운로드 경로 설정
            'ignoreerrors': True
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(urls)
        except Exception as e:
            print('error', e)

    def download_captions(self, priority_manually_created=True) -> None:
        lang = self.lang
        text = []
        wav_dir = os.path.join(settings.DATA_DIR, "wavs")
        file_list = os.listdir(wav_dir)
        file_list_wav = [file for file in file_list if file.endswith(".wav")]
        ytt_api = YouTubeTranscriptApi()
        for f in tqdm.tqdm(file_list_wav):
            transcript = Transcript("",0,
                "",
                None,
                None,
                True,
                [],)
            try:
                video = f.split(".wav")[0]
                transcript_list = ytt_api.list(video)
                if priority_manually_created:                  
                    try:
                        transcript = transcript_list.find_manually_created_transcript([lang])
                    except NoTranscriptFound:
                        msg = "Find generated transcript video {} because it has no manually generated subtitles"
                        print(msg.format(video))
                if transcript.language is None:
                    transcript = transcript_list.find_generated_transcript([lang])
                subtitle = transcript.fetch()
                for snippet in subtitle:
                    print(snippet.text)
                    print(snippet.start)    
                    print(snippet.duration)
            except Exception as e:
                print("error:", e)
            print(text)
        # df = pd.DataFrame({"id": video_id, "text": text, "start": start, "duration": duration, "name": full_names})
        # text_dir = os.path.join(self.output_dir, "text")
        # makedirs(text_dir)

        # df.to_csv(text_dir + '/subtitle.csv', encoding='utf-8')
        # res = [i + '|' + j for i, j in zip(names, text)]
        # df2 = pd.DataFrame({"name": res})
        # df2.to_csv(os.path.join(self.output_dir, 'metadata.csv'), encoding='utf-8', header=False, index=False)
        # file_data = OrderedDict()
        # for i in range(df.shape[0]):
        #     file_data[df['name'][i]] = df['text'][i]
        # with open(os.path.join(self.output_dir, 'alignment.json'), 'w', encoding="utf-8") as make_file:
        #     json.dump(file_data, make_file, ensure_ascii=False, indent="\n")

        # print(os.path.basename(self.output_dir) + ' channel was finished')
    def audio_split(self, parallel=False) -> None:
        base_dir = self.output_dir + '/wavs/*.wav'
        audio_paths = glob(base_dir)
        audio_paths.sort()
        fn = partial(split_with_caption)
        parallel_run(fn, audio_paths, desc="Split with caption", parallel=parallel)