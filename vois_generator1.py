import os
from elevenlabs import ElevenLabs

# Tvůj API klíč z ElevenLabs
api_key = os.getenv("ELEVENLABS_API_KEY")

# Vytvoření klienta
client = ElevenLabs(api_key=api_key)

# Vygeneruj audio výstup
response = client.text_to_speech.convert(
    voice_id="WzsP0bfiCpSDfNgLrUuN",  # např. hlas "Adam"
    model_id="eleven_multilingual_v2",
    optimize_streaming_latency=0,
    text="Ty blázne!"
)

# Ulož audio do souboru
with open("scene1.mp3", "wb") as f:
    for chunk in response:
        f.write(chunk)
