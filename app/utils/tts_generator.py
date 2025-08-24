import os
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code="a")

def generate_tts_kokoro(text):
    generator = pipeline(text, voice="af_heart")
    audio_filename = f"tts_audio/output_{abs(hash(text))}.wav"
    full_path = os.path.join("media", audio_filename)

    # generator yields tuples (gs, ps, audio)
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write(full_path, audio, 24000)

    return audio_filename
