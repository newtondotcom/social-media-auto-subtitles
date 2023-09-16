import os
from typing import Iterator, TextIO
import random

styles = ["Default", "Tilte-left", "Tilte-right"]

def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    for i, segment in enumerate(transcript, start=1):
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
            f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )

def write_ass(transcript: Iterator[dict], file: TextIO):
    file.write("[Script Info]\n")
    file.write("ScriptType: v4.00\n")
    file.write("Collisions: Normal\n")
    file.write("PlayDepth: 0\n")
    file.write("\n")
    file.write("[V4+ Styles]\n")
    file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding, WrapStyle\n")
    file.write("Style: Default, Arial, 21, &H00FF0000, &H000000FF, &H00000000, &H80000000, -1, 0, 0, 0, 100, 100, 0, 0.00, 1, 3, 1, 3, 30, 30, 30, 0, 2\n")
    file.write("Style: Tilte-left, Arial, 21, &H00FF0000, &H000000FF, &H00000000, &H80000000, -1, 0, 0, 0, 100, 100, 0, 7.00, 1, 3, 1, 3, 30, 30, 30, 0, 2\n")
    file.write("Style: Tilte-right, Arial, 21, &H00FF0000, &H000000FF, &H00000000, &H80000000, -1, 0, 0, 0, 100, 100, 0, -7.00, 1, 3, 1, 3, 30, 30, 30, 0, 2\n")
    file.write("\n")
    file.write("[Events]\n")
    file.write("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n")

    previous_end = "00:00:00.000"

    for i, segment in enumerate(transcript, start=1):
        counter = 0
        start_time = format_timestamp(segment['start'], always_include_hours=True)
        end_time = format_timestamp(segment['end'], always_include_hours=True)
        text = segment['text'].strip().replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').replace('-->', '->')
        delta = abs(convert_ms(start_time) - convert_ms(end_time))
        delta_word = delta/text.count(" ")//11
        boiler = "{\q1\\be1\\b700\shad10\\a11\k"+str(int(delta_word))+"}"
        emoji = r" {\frz345}\u1F468 "
        text =boiler+text.upper().replace(" "," "+boiler)
        text = text.split(" ")
        length = len(text)
        while counter < length:
            style = styles[random.randint(0,2)]
            localcount = random.randint(1, 3)
            if counter + localcount > length:
                localcount = length - counter
            localstart = add_n_ms(start_time,counter*delta_word)
            localend = add_n_ms(localstart,localcount*delta_word)
            localtext = " ".join(text[counter:counter+localcount])
            file.write(f"""Dialogue: 0,{localstart},{localend},{style},,50,50,20,,{localtext}"""+  "\n")
            counter += localcount       



def filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def convert_ms(time):
    parts = time.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split(".")[0])
    ms = int(parts[2].split(".")[1])
    return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

def add_n_ms(time, n):
    total_ms = convert_ms(time) + n
    new_hours, remainder = divmod(total_ms, 3600000)
    new_minutes, remainder = divmod(remainder, 60000)
    new_seconds, remainder = divmod(remainder, 1000)
    new_ms = remainder
    new_time = f"{int(new_hours):02d}:{int(new_minutes):02d}:{int(new_seconds):02d}.{int(new_ms):03d}"
    return new_time