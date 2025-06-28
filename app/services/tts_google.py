from google.cloud import texttospeech


def synthesize_speech_google(text: str) -> bytes:
    """
    Synthesizes speech from the input string of text using Google Cloud TTS.

    Args:
        text: The text to synthesize.

    Returns:
        The audio content in bytes (MP3 format).
    """
    print("Initializing Google Text-to-Speech client...")
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    print(f"Synthesizing speech for text: '{text[:100]}...'")
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    print("Speech synthesis successful.")

    return response.audio_content