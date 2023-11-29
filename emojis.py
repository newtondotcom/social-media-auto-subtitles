import subprocess
from utils import *

path_emojis = "emojis/images/"
image_list = [("1", 1.523, 5.518), ("2", 10.5, 15.5), ("3", 20.5, 25.5)]

emoji_size = 72

y_offset = 10

def overlay_images_on_video(in_path, out_path, image_list, width, height,ass):
    image_list = [(path_emojis + image + ".png", start_time, end_time) for image, start_time, end_time in image_list]

    swidth = (width-emoji_size)/2
    sheight = (height-emoji_size)/2 - y_offset
    
    filter_complex = "[0:v]ass='" + ass + "'[subtitle];"
    for idx, (image_name, start_time, end_time) in enumerate(image_list):
        previous_video = f"[subtitle]" if idx == 0 else f"[{idx}v]"
        filter_complex += f"{previous_video}[{idx + 1}:v]overlay={swidth}:{sheight}:enable='between(t,{start_time},{end_time})'"
        if idx < len(image_list) - 1:
            filter_complex += f"[{idx + 1}v];"
        else:
            filter_complex += ";"

    # Build the complete ffmpeg command
    cmd = (
        f"ffmpeg -i {in_path} {' '.join(['-i ' + image for image, _, _ in image_list])} "
        f"-filter_complex \"{filter_complex}\" -c:a copy {out_path} -y"
    )
    print(cmd)
    subprocess.run(cmd, shell=True)



