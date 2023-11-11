# audio_extraction.py
from pydub import AudioSegment

def extract_audio_from_video(video_path, output_path):
    AudioSegment.converter = r"D:\testapi\ffmpeg.exe"
    AudioSegment.ffprobe = r"D:\testapi\ffprobe.exe"

    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export(output_path, format="wav")