from utils import *
from gen import *

video_file = "input/test4.mp4"

audio_paths = get_audio([video_file])
audio_path = audio_paths[video_file]

words = get_transcribe(audio_path)

ass_path = "temp/"
ass_path = os.path.join(ass_path, f"{filename(video_file)}.ass")

with open(ass_path,"w", encoding="utf-8") as ass:
    write_ass(file=ass,words=words)

gen_video(path=video_file,ass_path=ass_path)