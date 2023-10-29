import whisperx
import gc 

device = "cpu"  # "cuda" or "cpu"
batch_size = 8 # reduce if low on GPU mem, before 16
compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy), before float16

def get_transcribe(audio_file):
    # 1. Transcribe with original whisper (batched), medium model is "medium"
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)

    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # delete model if low on GPU resources
    # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

    return result['segments']

