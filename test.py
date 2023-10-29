import whisperx
import gc 

device = "cpu" 
audio_file = "output.wav"
batch_size = 8 # reduce if low on GPU mem, before 16
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy), before float16

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("large-v2", device, compute_type=compute_type)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

print(result["segments"]) # after alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

# 3. Assign speaker labels
#diarize_model = whisperx.DiarizationPipeline(use_auth_token=YOUR_HF_TOKEN, device=device)

# add min/max number of speakers if known
#diarize_segments = diarize_model(audio)
# diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

#result = whisperx.assign_word_speakers(diarize_segments, result)
#print(diarize_segments)
#print(result["segments"]) # segments are now assigned speaker IDs

styles = ["Default", "Tilte-left", "Tilte-right"]

import random
import os
from typing import Iterator, TextIO

def filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def write_ass(file: TextIO):
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
    
    for s in result["segments"]:
        sentence_start = s['start']
        sentence_end = s['end']
        sentence_text = s['text']
        for segment in s['words']:
            word = segment['word']
            if len(segment)==1:
                break
            start = segment['start']
            end = segment['end']
            delta = (end - start) * 1000
            boiler = "{\q1\\be1\\b700\shad10\\a11\k"+str(int(delta))+"}"
            emoji = r" \{\frz345}\u1F468 "
            text =boiler+word.upper().replace(" "," "+boiler)
            style = styles[random.randint(0,2)]
            file.write(f"""Dialogue: 0,{start},{end},{style},,50,50,20,,{text}"""+  "\n")
            
ass_path = "temp/"
path = "test"
ass_path = os.path.join(ass_path, f"{filename(path)}.ass")
with open(ass_path,"w", encoding="utf-8") as ass:
            write_ass(file=ass)