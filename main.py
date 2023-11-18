from utils import *
from gen import *
from silent import *

video_file = "input/palma.mp4"

audio_paths = get_audio([video_file])
audio_path = audio_paths[video_file]

words = get_transcribe(audio_path)

ass_path = "temp/"
ass_path = os.path.join(ass_path, f"{filename(video_file)}.ass")

with open(ass_path,"w", encoding="utf-8") as ass:
    write_ass(file=ass,words=words)

out_path_uncut = gen_video(path=video_file,ass_path=ass_path)
out_path_cut = ""
silence(out_path_uncut,out_path_cut)