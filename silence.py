from pydub import AudioSegment, silence

myaudio = AudioSegment.from_wav("temp/test2.wav")

silence = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=myaudio.dBFS)

silence = [((start/1000),(stop/1000)) for start,stop in silence] #convert to sec

print(silence)