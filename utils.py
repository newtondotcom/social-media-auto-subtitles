import os
import ffmpeg
from typing import TextIO
import random
import subprocess
import cv2
from styles import *

def filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def time_to_hhmmss(date):
    data = str(date)
    second = int(date)
    ms = int((date - second) * 100)
    minutes = int(second) // 60
    second = int(second) % 60
    return f"00:{minutes}:{second}.{ms}" 

def get_audio(paths):
    audio_paths = {}

    if not os.path.exists("temp/"):
        os.makedirs("temp/")
        
    for path in paths:
        print(f"Extracting audio from {filename(path)}...")
        output_path = os.path.join("temp/", f"{filename(path)}.wav")
        ffmpeg.input(path).output(
            output_path,
            acodec="pcm_s16le", ac=1, ar="16k"
        ).run(quiet=True, overwrite_output=True)

        audio_paths[path] = output_path

    return audio_paths


styles = gen_styles()

def write_ass(file: TextIO, words):
    file.write("[Script Info]\n")
    file.write("ScriptType: v4.00\n")
    file.write("Collisions: Normal\n")
    file.write("PlayDepth: 0\n")
    file.write("\n")
    file.write("[V4+ Styles]\n")
    file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding, WrapStyle\n")
    for j in styles:
        file.write(j)
    file.write("\n")
    file.write("[Events]\n")
    file.write("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")

    print(words)
    
    for s in words:
        for segment in s['words']:
            word = segment['word']
            if len(segment)==1:
                break
            start = segment['start']
            end = segment['end']
            #tab.append([start,end,word])
            delta = (end - start) * 1000
            boiler = "{\q1\\b700\shad1\\a11\k"+str(int(delta))+"}"
            emoji = r" \{\frz345}\u1F468 "
            text =boiler+word.upper().replace(" "," "+boiler)
            style = "s"+str(random.randint(0,len(styles)))
            file.write(f"""Dialogue: 0,{time_to_hhmmss(start)},{time_to_hhmmss(end)},{style},,50,50,20,,{text}"""+  "\n")


def gen_video(path,ass_path):
    output_dir = "output/"
    out_path = os.path.join(output_dir, f"{filename(path)}ASS.mp4")
    ffmpeg_cmd = [
            "ffmpeg",
            "-i", path,
            #"-vf", f"ass={ass_path}:fontsdir=static/NotoColorEmoji-Regular.ttf",
            "-vf", f"ass={ass_path}",
            "-c:a", "copy",
            "-y",
            out_path
    ]
    subprocess.run(ffmpeg_cmd, check=False)
    return out_path
    
def clean_temp(path):
    None
    
def get_dimensions(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
    else:
        width = int(cap.get(3))  # 3 corresponds to CV_CAP_PROP_FRAME_WIDTH
        height = int(cap.get(4))  # 4 corresponds to CV_CAP_PROP_FRAME_HEIGHT

        print(f"Video Dimensions (Width x Height): {width} x {height}")

        # Release the video capture object
        cap.release()
        return width,height
    

def juxtaposer_mots(tab, new_tab, seuil, j, moyenne_time, moyenne_length):
    def is_below_threshold(word, next_word=None):
        if next_word is None:
            return word[1] - word[0] < moyenne_time or len(word[2]) < moyenne_length
        else:
            return next_word[0] - word[1] < seuil

    group = [tab[j]]
    if not is_below_threshold(tab[j]) or j == len(tab) - 1:
        new_tab.append(group)
        return 0

    mots_a_juxtaposer = min(4, len(tab) - j)
    retenue = 0

    for i in range(1, mots_a_juxtaposer):
        current_word = tab[j + i]
        previous_word = tab[j + i - 1]

        if is_below_threshold(current_word) and is_below_threshold(previous_word, current_word):
            group.append(current_word)
            retenue += 1
        else:
            break

    new_tab.append(group)
    return retenue