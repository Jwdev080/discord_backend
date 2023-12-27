import requests
from pydub import AudioSegment

def TexttoAudio(text, sex, age, random_index,filename):

    voice_id_female_young = ["21m00Tcm4TlvDq8ikWAM", "AZnzlk1XvdvUeBnXmlld", "EXAVITQu4vr4xnSDxMaL", 
                            "XrExE9yKIg1WjnnlVkGX",  "LcfcDJNUP1GQjkzn1xUU", "MF3mGyEYCl7XYWbV9V6O",
                            "jBpfuIE2acCO8z3wKNLl", "piTKgcLEGmPE4e6mEKli", "oWAxZDx7w5VEj9dCyTzz",
                            "jsCqWAovK2LkecY7zXl4"]
    voice_id_female_mid = ["pMsXgVXv3BLzUgSXRplE"]

    voice_id_male_young = ["GBv7mTt0atIp3Br8iCZE", "VR6AewLTigWG4xSOukaG", "ErXwobaYiN019PkySvjV",
                           "SOYHLrjzK2X1ezoPC6cr", "TX3LPaxmHKxFdv7VOQHJ", "TxGEqnHWrfWFTfGW9XjX",
                           "g5CIjZEefAph4nQFvHAz"]
    voice_id_male_mid = ["N2lVS1w4EtoT3dr4eOWO", "ODq5zmih8GrVes37Dizd", "z9fAnlkpzviPz146aGWa",
                          "2EiwWnXFnvU5JabPnv8n", "pNInz6obpgDQGcFmaJgB", "wViXBPUzp2ZZixB1xQuM"]
    voice_id_male_old = ["flq6f7yk4E4fJM5XTYuZ", "t0jbNlBVZ17f02VDIeMI"]

    voice_id = ""
    if sex == "Male":
        if age == "18-30":
            voice_id =  voice_id_male_young[random_index]
        if age == "31-45":
            voice_id =  voice_id_male_mid[random_index]
        if age =="46+":
            voice_id = voice_id_male_old[random_index]
            
    if sex == "Female":
        if age == "18-30":
            voice_id =  voice_id_female_young[random_index]
        if age == "31-45" or "46+":
            voice_id =  voice_id_female_mid[0]


    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "cb7f39e98e9a0ce626172c16f07e39ca"
    }
    data = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }
    response = requests.post(url, json=data, headers=headers)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def get_mp3_duration(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    duration_in_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
    return duration_in_seconds

def concatenate_mp3_files(input_files, output_file):
    # Create an empty AudioSegment to store the concatenated audio
    concatenated_audio = AudioSegment.silent()

    # Concatenate each MP3 file
    for mp3_file in input_files:
        audio_segment = AudioSegment.from_mp3(mp3_file)
        concatenated_audio += audio_segment

    # Export the concatenated audio to a new MP3 file
    concatenated_audio.export(output_file, format="mp3")