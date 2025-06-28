import ffmpeg
import tempfile
import os

def _get_background_music(keywords: list) -> str:
    """
    Simulates selecting background music based on content keywords.
    In a real implementation, this could search a library or use an API.
    """
    print(f"[Audio Enhancer] Searching for music with keywords: {keywords}")
    # For this example, we'll just use a placeholder.
    # This would be a path to a file in your Docker container or a URL.
    # For simplicity, we assume a local file path.
    # You would need to add music files to your project.
    # Let's assume we have a file named 'uplifting-music.mp3'
    music_path = "path/to/your/music/uplifting-music.mp3"
    print(f"[Audio Enhancer] Selected music: {music_path}")
    return music_path

def mix_audio_with_music(speech_audio_bytes: bytes, keywords: list = None) -> bytes:
    """
    Mixes speech audio with background music using ffmpeg.
    """
    if not keywords:
        keywords = ["uplifting", "corporate"]

    try:
        music_file_path = _get_background_music(keywords)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as speech_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as output_file:
            speech_file.write(speech_audio_bytes)

            # ffmpeg command to mix audio
            input_speech = ffmpeg.input(speech_file.name)
            input_music = ffmpeg.input(music_file_path)
            mixed_audio = ffmpeg.filter([input_speech, input_music], 'amix', duration='first', dropout_transition=2)
            
            ffmpeg.output(mixed_audio, output_file.name, acodec='libmp3lame').run(overwrite_output=True, quiet=True)
            
            return output_file.read()
    except Exception as e:
        print(f"ERROR during audio mixing: {e}. Returning original speech.")
        return speech_audio_bytes